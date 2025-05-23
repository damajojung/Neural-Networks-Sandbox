import os
import yaml
import time
import asyncio
import fal_client
import requests
import random


async def subscribe(prompt, seed, latent_width ,latent_height):
    handler = await fal_client.submit_async(
        "comfy/damajojung/falniimgratioseed",
        arguments={
            "prompt": prompt,
            "seed": seed,
            "latent_width": latent_width,
            "latent_height": latent_height
        },
    )

    async for event in handler.iter_events(with_logs=True):
        print(event)

    result = await handler.get()

    print(result)

    # Extracting the image URL
    key = list(result['outputs'].keys())[0]  # Dynamically get the first key
    image_url = result['outputs'][key]['images'][0]['url']

    print(f"Image URL: {image_url}")

    return image_url


async def main():
    # Set up environment
    with open(os.path.join(os.getcwd(), 'tokens.yml')) as f:
        tokens = yaml.safe_load(f)

    os.environ["FAL_KEY"] = tokens['FAL_KEY'][0]

    current_request = str(round(time.time()))
    current_path = os.getcwd()
    current_request_path = os.path.join(current_path, current_request)

    if not os.path.exists(current_request_path):
        os.makedirs(current_request_path)

    # Load prompts
    promt_folder = "promts"
    file_name = "api_promts.yml"
    file_path = os.path.join(os.getcwd(), promt_folder, file_name)

    with open(file_path, "r") as f:
        api_specs = yaml.safe_load(f)

    # Set up logs folder
    logs_folder = "api_logs"
    file_name_logs = "logs.txt"
    logs_path = os.path.join(current_request_path, logs_folder)

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    
    img_folder = 'images'
    img_path = os.path.join(current_request_path, img_folder)

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    # Process prompts
    logs = []
    for p in api_specs['promts']:

        # if you want to use a lora key word 
        # p = f"Klett & Balmer illustration style, {p}"
        print(p)
        # seed starts at 0 
        img_seed = 0

        for ar in api_specs['aspect_ratios']:
            img_ratio = ar["aspect_ratio"]
            img_width = ar["width"]
            img_height = ar["height"]
            img_seed = img_seed

            a = time.time()

            # Call the subscribe function
            image_url = await subscribe(
                prompt = p,
                seed = img_seed,
                latent_width = img_width,
                latent_height = img_height
                )

            b = time.time()
            elapsed_time = b - a
            print(f"Inference Time: {round(elapsed_time, 1)} seconds")
            logs.append({"promt": p, 
                         "seed": img_seed, 
                         "img_width": img_width,
                         "img_height": img_height,
                         'img_ratio': img_ratio,
                         "elapsed_time" : elapsed_time})

            # Download and save the image
            response = requests.get(image_url)
            if response.status_code == 200:
                output_file = f"img_{round(a)}.png"
                with open(os.path.join(img_path, output_file), "wb") as f:
                    f.write(response.content)
                print(f"Image saved as {output_file}")
            else:
                print(f"Failed to download the image. Status code: {response.status_code}")

            
            img_seed += 1

    # Save the inference times to the log file
    with open(os.path.join(logs_path, file_name_logs), "w") as file:
        for item in logs:
            file.write(f"{item}\n")


if __name__ == "__main__":
    asyncio.run(main())
