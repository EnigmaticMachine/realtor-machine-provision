import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import random
import os
import uuid


def generate_batch_of_images(image_path, folder_name):
    # Open an image file
    with Image.open(image_path) as img:
        # Get image size
        width, height = img.size

    width = width * 1
    height = height * 1

    with open(image_path, "rb") as image_file:
        byte_data = image_file.read()
        input_image_b64 = base64.b64encode(byte_data).decode("utf-8")

    payload = {
        "init_images": [input_image_b64],
        "prompt": "modern interior, ikea, interior design magazine, 8k",
        "negative_prompt": "old",
        "steps": 40,
        "seed": 1223,
        "width": width,
        "height": height,
        "save_images": False,
        "denoising_strength": 0.48,
        "batch_size": 2,
        "n_iter": 8,
        "sampler_index": "DDIM",
    }

    response = requests.post(url=f"{url}/sdapi/v1/img2img", json=payload)
    r = response.json()

    # parts = image_path.split("/")
    # folder_name = parts[3]
    
    # Generate a random UUID
    my_uuid = uuid.uuid4()

    # Convert the UUID to a string
    my_uuid_str = str(my_uuid)

    # Split the string on the '-' character and take the first part
    first_part = my_uuid_str.split('-')[0]                              
    folder_name = first_part

    directory_path = f"/root/stable-diffusion-webui/outputs/{folder_name}"

    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.mkdir(directory_path)

    print("response: ", r)

    for i in r["images"]:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {"image": "data:image/png;base64," + i}
        response2 = requests.post(url=f"{url}/sdapi/v1/png-info", json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        random_number = random.randint(1, 100)

        image.save(
            f"{directory_path}/visualisation_{random_number}.png", pnginfo=pnginfo
        )


url = "http://127.0.0.1:7860"

# Specify the directory
directory = "/root/stable-diffusion-webui/inputs"

# Get list of all files in directory
files_in_directory = os.listdir(directory)

# Create a list to store the full paths
full_paths = []

# Loop through all files
for file in files_in_directory:
    # Combine the directory path with the filename
    full_path = os.path.join(directory, file)
    # Add the full path to the list
    full_paths.append(full_path)

# Enumerate and print the list of full paths
for i, image_path in enumerate(full_paths):
    print("image_path", image_path)
    generate_batch_of_images(image_path=image_path, folder_name=i)
