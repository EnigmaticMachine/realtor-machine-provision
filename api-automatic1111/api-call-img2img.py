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

    # Check if either side is greater than 900
    if max(width, height) > 900:
        # Calculate scaling factor
        scale_factor = 900 / max(width, height)
        width = int(width * scale_factor)
        height = int(height * scale_factor)
    else:
        # If neither side is greater than 900, do nothing
        scale_factor = 1
        width = int(width * scale_factor)
        height = int(height * scale_factor)

    # muliply_resolution = 1
    # width = width * muliply_resolution
    # height = height * muliply_resolution

    with open(image_path, "rb") as image_file:
        byte_data = image_file.read()
        input_image_b64 = base64.b64encode(byte_data).decode("utf-8")

    payload = {
        "init_images": [input_image_b64],
        "prompt": "ikea style, Scandinavian interior, product photography, Nikon",
        "steps": 40,
        "seed": 12159,
        "width": width,
        "height": height,
        "sampler_name": "DPM++ SDE Karras",
        "batch_size": 2,
        "n_iter": 3,
        "cfg_scale": 6,
        "denoising_strength": 0.65,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": True,
                        "module": "canny",
                        "model": "control_sd15_canny [fef5e48e]",
                        "control_mode": "My prompt is more important",
                        "processor_res": 1024,
                    }
                ]
            }
        },
    }

    response = requests.post(url=f"{url}/sdapi/v1/img2img", json=payload)
    # response = requests.post(url=f"{url}/controlnet/detect", json=payload)
    r = response.json()

    # parts = image_path.split("/")
    # folder_name = parts[3]

    # Generate a random UUID
    my_uuid = uuid.uuid4()

    # Convert the UUID to a string
    my_uuid_str = str(my_uuid)

    # Split the string on the '-' character and take the first part
    first_part = my_uuid_str.split("-")[0]
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
