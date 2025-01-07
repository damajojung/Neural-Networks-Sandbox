from diffusers import StableDiffusionPipeline
import torch

# Load the diffusion pipeline from Hugging Face
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# Generate an image
prompt = "A futuristic cityscape at sunset"
image = pipe(prompt).images[0]

# Save the image
image.save("output.png")
print("Image saved as output.png")
