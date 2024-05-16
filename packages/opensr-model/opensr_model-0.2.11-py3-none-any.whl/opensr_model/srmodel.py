import pathlib
from typing import Union
import requests
import torch
from opensr_model.diffusion.latentdiffusion import LatentDiffusion
from skimage.exposure import match_histograms
import torch.utils.checkpoint as checkpoint
from opensr_model.diffusion.utils import DDIMSampler
from tqdm import tqdm
import numpy as np
from typing import Literal
import shutil
import random
import numpy as np
from einops import rearrange
from opensr_model.utils import assert_tensor_validity
from opensr_model.utils import revert_padding



class SRLatentDiffusion(torch.nn.Module):
    def __init__(self, bands: str = "10m", device: Union[str, torch.device] = "cpu"):
        super().__init__()

        # Set parameters depending on band selection
        self.band_config = bands
        assert self.band_config in ["10m", "20m"], "band selection incorrect"

        # Set up the model
        first_stage_config, cond_stage_config = self.set_model_settings()
        self.model = LatentDiffusion(
            first_stage_config,
            cond_stage_config,
            timesteps=1000,
            unet_config=cond_stage_config,
            linear_start=0.0015,
            linear_end=0.0155,
            concat_mode=True,
            cond_stage_trainable=False,
            first_stage_key="image",
            cond_stage_key="LR_image",
        )

        # set up mean/std - TODO: remove in future
        #self.mean, self.std = self.set_mean_std()

        # Set up the model for inference
        self.device = device # set self device
        self.model.device = device # set model device as selected
        self.model = self.model.to(device) # move model to device
        self.model.eval() # set model state
        self._X = None # placeholder for LR image
        self.encode_conditioning = True # encode LR images before dif?
        self.sr_type = "SISR" # set wether SISR or MIRS

    def set_model_settings(self):
        # set up model settings
        if self.band_config == "10m":
            print("Creating model for 4x 10m bands...")
            first_stage_config = {
                "embed_dim":4,
                "double_z": True,
                "z_channels": 4,
                "resolution": 256,
                "in_channels": 4,
                "out_ch": 4,
                "ch": 128,
                "ch_mult": [1, 2, 4],
                "num_res_blocks": 2,
                "attn_resolutions": [],
                "dropout": 0.0,
            }
            cond_stage_config = {
                "image_size": 64,
                "in_channels": 8,
                "model_channels": 160,
                "out_channels": 4,
                "num_res_blocks": 2,
                "attention_resolutions": [16, 8],
                "channel_mult": [1, 2, 2, 4],
                "num_head_channels": 32,
            }
            # set transform for 10m
            from opensr_model.utils import linear_transform_4b
            self.linear_transform = linear_transform_4b

            return first_stage_config, cond_stage_config

        if self.band_config == "20m":
            print("Creating model for 6x 20m bands...")
            first_stage_config = {
                "embed_dim":6,
                "double_z": True,
                "z_channels": 6,
                "resolution": 512,
                "in_channels": 6,
                "out_ch": 6,
                "ch": 128,
                "ch_mult": [1, 2, 4],
                "num_res_blocks": 2,
                "attn_resolutions": [],
                "dropout": 0.0,
            }
            cond_stage_config = {
                "image_size": 64,
                "in_channels": 12,
                "model_channels": 160,
                "out_channels": 6,
                "num_res_blocks": 2,
                "attention_resolutions": [16, 8],
                "channel_mult": [1, 2, 2, 4],
                "num_head_channels": 32,
            }
            # set transform for 20m
            from opensr_model.utils import linear_transform_6b
            self.linear_transform = linear_transform_6b
            # return configs
            return first_stage_config, cond_stage_config

        
    def _tensor_encode(self,X: torch.Tensor):
        # set copy to model
        self._X = X.clone()
        # normalize image
        X_enc = self.linear_transform(X, stage="norm")
        # encode LR images
        self.encode_conditioning = True
        if self.encode_conditioning==True and self.sr_type=="SISR":
            # try to upsample->encode conditioning
            X_int = torch.nn.functional.interpolate(X, size=(X.shape[-1]*4,X.shape[-1]*4), mode='bilinear', align_corners=False)
            print(X_int.shape)
            # encode conditioning
            X_enc = self.model.first_stage_model.encode(X_int).sample()
        # move to same device as the model
        X_enc = X_enc.to(self.device)
        return X_enc

    def _tensor_decode(self, X_enc: torch.Tensor, spe_cor: bool = True):       
        # Decode
        X_dec = self.model.decode_first_stage(X_enc)
        X_dec = self.linear_transform(X_dec, stage="denorm")
        # Apply spectral correction
        if spe_cor:
            for i in range(X_dec.shape[1]):
                X_dec[:, i] = self.hq_histogram_matching(X_dec[:, i], self._X[:, i])
        # If the value is negative, set it to 0
        X_dec[X_dec < 0] = 0    
        return X_dec
    
    def _prepare_model(
        self,
        X: torch.Tensor,
        eta: float = 1.0,
        custom_steps: int = 100,
        verbose: bool = False 
    ):
        # Create the DDIM sampler
        ddim = DDIMSampler(self.model)
        
        # make schedule to compute alphas and sigmas
        ddim.make_schedule(ddim_num_steps=custom_steps, ddim_eta=eta, verbose=verbose)
        
        # Create the HR latent image
        latent = torch.randn(X.shape, device=X.device)
                
        # Create the vector with the timesteps
        timesteps = ddim.ddim_timesteps
        time_range = np.flip(timesteps)
        
        return ddim, latent, time_range

    def _attribution_methods(
        self,
        X: torch.Tensor,
        grads: torch.Tensor,
        attribution_method: Literal[
            "grad_x_input", "max_grad", "mean_grad", "min_grad"            
        ],
    ):
        if attribution_method == "grad_x_input":
            return torch.norm(grads * X, dim=(0, 1))
        elif attribution_method == "max_grad":
            return grads.abs().max(dim=0).max(dim=0)
        elif attribution_method == "mean_grad":
            return grads.abs().mean(dim=0).mean(dim=0)
        elif attribution_method == "min_grad":
            return grads.abs().min(dim=0).min(dim=0)
        else:
            raise ValueError(
                "The attribution method must be one of: grad_x_input, max_grad, mean_grad, min_grad"
            )
    
    def explainer(
        self,
        X: torch.Tensor,
        mask: torch.Tensor,
        eta: float = 1.0,
        temperature: float = 1.0,
        custom_steps: int = 100,
        steps_to_consider_for_attributions: list = list(range(100)),
        attribution_method: Literal[
            "grad_x_input", "max_grad", "mean_grad", "min_grad"
        ] = "grad_x_input",      
        verbose: bool = False,
        enable_checkpoint = True,
        histogram_matching=True        
    ):  
        # Normalize and encode the LR image
        X = X.clone()
        Xnorm = self._tensor_encode(X)
        
        # ddim, latent and time_range
        ddim, latent, time_range = self._prepare_model(
            X=Xnorm, eta=eta, custom_steps=custom_steps, verbose=verbose
        )
                    
        # Iterate over the timesteps
        container = []
        iterator = tqdm(time_range, desc="DDIM Sampler", total=custom_steps,disable=True)
        for i, step in enumerate(iterator):
            
            # Activate or deactivate gradient tracking
            if i in steps_to_consider_for_attributions:
                torch.set_grad_enabled(True)
            else:
                torch.set_grad_enabled(False)
            
            # Compute the latent image
            if enable_checkpoint:
                outs = checkpoint.checkpoint(
                    ddim.p_sample_ddim,
                    latent,
                    Xnorm,
                    step,
                    custom_steps - i - 1,
                    temperature,
                    use_reentrant=False,
                )
            else:                
                outs = ddim.p_sample_ddim(
                    x=latent,
                    c=Xnorm,
                    t=step,
                    index=custom_steps - i - 1,
                    temperature=temperature
                )
            latent, _ = outs
            
            
            if i not in steps_to_consider_for_attributions:
                continue
            
            # Apply the mask
            output_graph = (latent*mask).mean()
            
            # Compute the gradients
            grads = torch.autograd.grad(output_graph, Xnorm, retain_graph=True)[0]
            
            # Compute the attribution and save it
            with torch.no_grad():
                to_save = {
                    "latent": self._tensor_decode(latent, spe_cor=histogram_matching),
                    "attribution": self._attribution_methods(
                        Xnorm, grads, attribution_method
                    )
                }
            container.append(to_save)
        
        return container

    @torch.no_grad()
    def forward(
        self,
        X: torch.Tensor,
        eta: float = 1.0,
        custom_steps: int = 100,
        temperature: float = 1.0,
        histogram_matching: bool = True,
        save_iterations: bool = False,
        verbose: bool = False
    ):
        """Obtain the super resolution of the given image.

        Args:
            X (torch.Tensor): If a Sentinel-2 L2A image with reflectance values
                in the range [0, 1] and shape CxWxH, the super resolution of the image
                is returned. If a batch of images with shape BxCxWxH is given, a batch
                of super resolved images is returned.
            custom_steps (int, optional): Number of steps to run the denoiser. Defaults
                to 100.
            temperature (float, optional): Temperature to use in the denoiser.
                Defaults to 1.0. The higher the temperature, the more stochastic
                the denoiser is (random noise gets multiplied by this).
            spectral_correction (bool, optional): Apply spectral correction to the SR
                image, using the LR image as reference. Defaults to True.

        Returns:
            torch.Tensor: The super resolved image or batch of images with a shape of
                Cx(Wx4)x(Hx4) or BxCx(Wx4)x(Hx4).
        """
        
        # Assert shape, size, dimensionality
        X,padding = assert_tensor_validity(X)

        # Normalize the image
        X = X.clone()
        Xnorm = self._tensor_encode(X)
        
        # ddim, latent and time_range
        ddim, latent, time_range = self._prepare_model(
            X=Xnorm, eta=eta, custom_steps=custom_steps, verbose=verbose
        )
        iterator = tqdm(time_range, desc="DDIM Sampler", total=custom_steps,disable=True)

        # Iterate over the timesteps
        if save_iterations:
            save_iters = []
            
        for i, step in enumerate(iterator):
            outs = ddim.p_sample_ddim(
                x=latent,
                c=Xnorm,
                t=step,
                index=custom_steps - i - 1,
                use_original_steps=False,
                temperature=temperature
            )
            latent, _ = outs
            
            if save_iterations:
                save_iters.append(
                    self._tensor_decode(latent, spe_cor=histogram_matching)
                )
        
        if save_iterations:
            return save_iters
        
        sr = self._tensor_decode(latent, spe_cor=histogram_matching)
        sr = revert_padding(sr,padding)
        return sr


    def hq_histogram_matching(
        self, image1: torch.Tensor, image2: torch.Tensor
    ) -> torch.Tensor:
        """Lazy implementation of histogram matching

        Args:
            image1 (torch.Tensor): The low-resolution image (C, H, W).
            image2 (torch.Tensor): The super-resolved image (C, H, W).

        Returns:
            torch.Tensor: The super-resolved image with the histogram of
                the target image.
        """

        # Go to numpy
        np_image1 = image1.detach().cpu().numpy()
        np_image2 = image2.detach().cpu().numpy()

        if np_image1.ndim == 3:
            np_image1_hat = match_histograms(np_image1, np_image2, channel_axis=0)
        elif np_image1.ndim == 2:
            np_image1_hat = match_histograms(np_image1, np_image2, channel_axis=None)
        else:
            raise ValueError("The input image must have 2 or 3 dimensions.")

        # Go back to torch
        image1_hat = torch.from_numpy(np_image1_hat).to(image1.device)

        return image1_hat

    def load_pretrained(self, weights_file: str):
        """
        Loads the pretrained model from the given path.
        """

        # download pretrained model
        #hf_model = "https://huggingface.co/isp-uv-es/opensr-model/resolve/main/sr_checkpoint.ckpt" # original one
        # create download link based on input 
        hf_model = str("https://huggingface.co/simon-donike/RS-SR-LTDF/resolve/main/"+str(weights_file))
        
        # download pretrained model
        if not pathlib.Path(weights_file).exists():
            print("Downloading pretrained weights from: ", hf_model)
            with open(weights_file, "wb") as f:
                f.write(requests.get(hf_model).content)

        weights = torch.load(weights_file, map_location=self.device)["state_dict"]

        # Remote perceptual tensors from weights
        for key in list(weights.keys()):
            if "loss" in key:
                del weights[key]

        self.model.load_state_dict(weights, strict=True)
        print("Loaded pretrained weights from: ", weights_file)


# -----------------------------------------------------------------------------
# Logic to create PyTorch Lightning Model from dif model
# Logic to handle outputs from PL model and save them
# -----------------------------------------------------------------------------

import torch
import pytorch_lightning
from pytorch_lightning import LightningModule

class SRLatentDiffusionLightning(LightningModule):
    """
    This Pytorch Lightning Class wraps around the torch model to
    aid in distrubuted GPU processing and optimized dataloaders
    provided by PL.
    """
    def __init__(self,bands: str = "10m", device: Union[str, torch.device] = "cpu",
                 custom_steps: int = 100, temperature: float = 1.0):
        super().__init__()
        self.model = SRLatentDiffusion(bands=bands,device=device)
        self.model = self.model.eval()
        self.custom_steps = custom_steps
        self.temperature = temperature
        self.predict_dataset = None
        self.mode = "SR" # setting this hardcoded. If we're in xAI, this will get overwritten externally

    def forward(self, x,**kwargs):
        #print("Dont call 'forward' on the PL model, instead use 'predict'")
        return self.model(x,custom_steps=self.custom_steps)
    
    def load_pretrained(self, weights_file: str):
        self.model.load_pretrained(weights_file)
        print("PL Model: Model loaded from ", weights_file)

    def predict_step(self, x, idx: int = 0,**kwargs):
        # perform SR
        assert self.model.training == False, "Model in Training mode. Abort." # make sure we're in eval

        if self.mode=="SR":
            p = self.model.forward(x,custom_steps=self.custom_steps,temperature=self.temperature)
            return(p)
        if self.mode=="xAI":
            p = self.xai_step(x, idx)
            return(p)
    
    def xai_step(self, x, idx):
        no_uncertainty = 15 # amount of images to SR
        rand_seed_list = random.sample(range(1, 9999), no_uncertainty) # list of random seeds
        variations = [] # empty list to hold variations
        for i in range(no_uncertainty):
            # reseed random number generators for each iteration
            np.random.seed(rand_seed_list[i])
            torch.manual_seed(rand_seed_list[i])
            random.seed(rand_seed_list[i])
            pytorch_lightning.utilities.seed.seed_everything(seed=rand_seed_list[i],workers=True)
            
            sr = self.model.forward(x,custom_steps=self.custom_steps)
            sr = sr.squeeze(0)
            variations.append(sr.detach().cpu())
        variations = torch.stack(variations)
        # Get statistics for xAI
        srs_mean = variations.mean(dim=0)
        srs_stdev = variations.std(dim=0)
        lower_bound = srs_mean-srs_stdev
        upper_bound = srs_mean+srs_stdev
        interval_size = srs_stdev*2
        interval_size = interval_size.mean(dim=0).unsqueeze(0)
        return interval_size


"""
import torch
import os
from pytorch_lightning.callbacks import BasePredictionWriter
class CustomWriter(BasePredictionWriter):
    
    #- Applied after each predict step by the predict() of PL model
    #- this class needs as input the SR object created by opensr-utils
    #- it writes the results to a temporary folder
    #- it writes the results to the placeholder file at the end
    
    def __init__(self, sr_obj, write_interval="batch"):
        super().__init__(write_interval)
        self.sr_obj = sr_obj # save SR obj in class

        # create folder and info to save temporary results
        base_path = os.path.dirname(self.sr_obj.info_dict["sr_path"])
        self.temp_path = os.path.join(base_path,"tmp_sr")
        os.makedirs(self.temp_path, exist_ok=True)

        # if files exist in folder, remove them
        files = os.listdir(self.temp_path)
        for file in files:
            os.remove(os.path.join(self.temp_path,file))

    def write_on_batch_end(self, trainer,
                           pl_module, prediction,
                           batch_indices, batch,
                           batch_idx, dataloader_idx):
        try:
            prediction = prediction.cpu()
        except:
            pass

        # iterate over predictions and save them accordingly
        #for pred,idx in zip(prediction,batch_indices):
        #    self.sr_obj.sr_obj.fill_SR_overlap(pred,idx,self.sr_obj.info_dict)

        # create filename
        formatted_number_1 = "{:06}".format(batch_indices[0])
        formatted_number_2 = "{:04d}".format(len(batch_indices))
        filename = "batch{}__{}batches.pt".format(formatted_number_1,formatted_number_2)
        # create dictionary out of results and save to disk
        results_dict = {"sr":prediction,"batch_indices":batch_indices}
        torch.save(results_dict,os.path.join(self.temp_path,filename))
        
        # return nothing in order not to accumulate results
        return None
    
    #def write_all_to_placeholder(self):
    def on_predict_end(self, trainer, pl_module):
        
        #Custom function to be called after all predictions are done
        
        # run this only on one GPU
        if trainer.global_rank == 0:
            print("Running weighted Patching on Worker:",str(trainer.global_rank),"...")
            # read all files in folder
            files = os.listdir(self.temp_path)
            files = [file for file in files if file.endswith(".pt")] # keep only .pt files

            # iterate over files and save them to placeholder
            for file in tqdm(files,desc="Saving to PH"):
                # load file
                results_dict = torch.load(os.path.join(self.temp_path,file))
                # iterate over results and save them
                for pred,idx in zip(results_dict["sr"],results_dict["batch_indices"]):
                    self.sr_obj.sr_obj.fill_SR_overlap(pred,idx,self.sr_obj.info_dict)
            
            # delete temporary folder and all its contents
            # Make sure the path exists and is a directory
            if os.path.isdir(self.temp_path):
                import time 
                time.sleep(10)
                # Remove the folder and all its contents
                shutil.rmtree(self.temp_path)
                print(f"Data written to disk, temp folder deleted. Finished.")
            else:
                print(f"Data written to disk, temp folder not deleted.")
            return None

"""