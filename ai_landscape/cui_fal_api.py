import os
import yaml
import time
import asyncio
import fal_client
import requests


import asyncio
import fal_client

async def subscribe(promt):
    handler = await fal_client.submit_async(
        "comfy/damajojung/e1nileanfal",
        arguments={
            "prompt": promt
        },
    )

    async for event in handler.iter_events(with_logs=False):
        print(event)

    result = await handler.get()

    print(result)

    # Extracting the image URL
    key = list(result['outputs'].keys())[0]  # Dynamically get the first key
    image_url = result['outputs'][key]['images'][0]['url']

    # # Extracting the image URL
    # image_url = result['outputs']['82']['images'][0]['url']
    print(f"Image URL: {image_url}")

    return image_url


if __name__ == "__main__":

    #-----------------------------------------   set up environment
    # tokens must be in the same directory
    with open(os.path.join(os.getcwd(), 'tokens.yml')) as f:
        tokens = yaml.safe_load(f)
    
    # set the fal api key 
    os.environ["FAL_KEY"] = tokens['FAL_KEY'][0]


    # ---------------------------------------- load specs
    # Define the folder and file name
    folder = "promts"
    file_name = "api_promts.yml"

    # Construct the full file path
    file_path = os.path.join(os.getcwd(), folder, file_name)

    # Read the YAML file
    with open(file_path, "r") as f:
        api_specs = yaml.safe_load(f)
    

    # ------------------------------------------ logs
    logs_folder = "api_logs"
    file_name_logs = "logs.txt"
    file_path_logs = os.path.join(os.getcwd(), folder, file_name)

    # Check if the folder exists, and create it if it doesn't
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
        

    # ----------------------------------------- local variables
    # create empty list for tracking inference
    times = []

    # start process
    for p in api_specs['promts']:

        print(p)
        a = time.time()
        image_url = asyncio.run(subscribe(promt=p))
        b = time.time()

        c = b - a
        print(f'Inference Time: {round(c,1)} seconds')
        times.append(c)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"output_image_{round(a)}.png", "wb") as f:
                f.write(response.content)
            print("Image saved as output_image.png")
        else:
            print(f"Failed to download the image. Status code: {response.status_code}")

    
    # Save the list to the file
    with open(file_path_logs, "w") as file:
        for item in times:
            file.write(f"{item}\n")