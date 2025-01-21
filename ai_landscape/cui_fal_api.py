import os
import yaml
import time
import asyncio
import fal_client
import requests


import asyncio
import fal_client

async def subscribe():
    handler = await fal_client.submit_async(
        "comfy/damajojung/e1nileanfal",
        arguments={
            "prompt": "close up of a viking woman's face, ultra realistic"
        },
    )

    async for event in handler.iter_events(with_logs=True):
        print(event)

    result = await handler.get()

    print(result)

    # Extracting the image URL
    image_url = result['outputs']['82']['images'][0]['url']
    print(f"Image URL: {image_url}")

    return image_url


if __name__ == "__main__":

    with open(os.path.join(os.getcwd(), 'tokens.yml')) as f:
        tokens = yaml.safe_load(f)
    
    os.environ["FAL_KEY"] = tokens['FAL_KEY'][0]

    a = time.time()
    image_url = asyncio.run(subscribe())
    b = time.time()

    c = b - a
    print(f'Inference Time: {round(c,1)} seconds')

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(f"output_image_{round(a)}.png", "wb") as f:
            f.write(response.content)
        print("Image saved as output_image.png")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")