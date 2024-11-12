import os
import replicate
from replicate.client import Client
import yaml
import time

def getAuth():
        with open(os.path.join(os.getcwd(), 'tokens.yml')) as f:
            tokens = yaml.safe_load(f)
        os.environ["REPLICATE_API_TOKEN"] = tokens['REPLICATE_API_TOKEN'][0]
        replicate = Client(api_token=os.environ["REPLICATE_API_TOKEN"])
        return(replicate)

def getFluxSchnellImage(**kwargs):
        replicate = getAuth()
        
        default_input = {
                    "prompt": "",
                    "go_fast": True,
                    "megapixels": "1",
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "output_quality": 80,
                    "num_inference_steps": 4
                }
        
        default_input.update(**kwargs)

        output = replicate.run(
                "black-forest-labs/flux-schnell",
                input = default_input)
        
        return output

def getFluxDevImage(**kwargs):
        
        replicate = getAuth()
        
        default_input = {
        "prompt": "",
        "go_fast": True,
        "guidance": 3.5,
        "megapixels": "1",
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 80,
        "prompt_strength": 0.8,
        "num_inference_steps": 28
    }
        
        default_input.update(**kwargs)

        output = replicate.run(
                "black-forest-labs/flux-dev",
                input = default_input)
        
        return output


def getFluxProImage(**kwargs):
        
        replicate = getAuth()
        
        default_input = {
        "steps": 25,
        "width": 1024,
        "height": 1024,
        "prompt": "",
        "guidance": 3,
        "interval": 2,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 80,
        "safety_tolerance": 2,
        "prompt_upsampling": False
    }
        
        default_input.update(**kwargs)

        output = replicate.run(
                "black-forest-labs/flux-pro",
                input = default_input)
        
        return output