# # https://huggingface.co/stabilityai/stable-diffusion-2-depth

import torch
import requests
from PIL import Image
from diffusers import StableDiffusionDepth2ImgPipeline
import time
import requests
import os
import argparse
import json
import sys


pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-depth",
    torch_dtype=torch.float16,
).to("cuda")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
init_image = Image.open(requests.get(url, stream=True).raw)


def make_vizualization(titles):
    # Directory to save the files
    save_dir = "stablediffusion/inputs/"

    file_paths = []
    print("all links: ", titles)
    for title in titles:  # json_data['download_links']:
        print("title ", title)
        # Extract the file name from the URL
        local_path = os.path.join(save_dir, title)
        file_paths.append(local_path)

    for count, file in enumerate(file_paths):
        init_image = Image.open(file)

        prompt = "modern apartment"
        n_propmt = "bad, deformed, ugly, bad anotomy"
        image = pipe(
            prompt=prompt, image=init_image, negative_prompt=n_propmt, strength=0.9999
        ).images[0]
        image.save(f"stablediffusion/outputs/{titles[count]}")

        del image
        torch.cuda.empty_cache()
        time.sleep(2)


if __name__ == "__main__":
    titles = json.loads(sys.argv[1])
    print("sys.argv[1] ", sys.argv[1])
    print("titles ", titles)
    make_vizualization(titles)
