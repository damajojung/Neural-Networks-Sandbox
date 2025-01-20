import os
import yaml
import time
import asyncio
import fal_client
import requests


async def subscribe():
    handler = await fal_client.submit_async(
        "comfy/damajojung/e1nilean",
          arguments={
                "prompt": "a picture of deep space with many stars and colorful nebulas",
                "image_size": {
                    "width": 1024,
                    "height": 1024
                }
            }
    )

    async for event in handler.iter_events(with_logs=True):
        print(event)

    result = await handler.get()

    print(result)


if __name__ == "__main__":

    with open(os.path.join(os.getcwd(), 'tokens.yml')) as f:
        tokens = yaml.safe_load(f)
    
    os.environ["FAL_KEY"] = tokens['FAL_KEY'][0]

    asyncio.run(subscribe())