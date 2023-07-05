import json
import requests
import io
import base64

url = "http://127.0.0.1:7860"
endpoint = "/sdapi/v1/refresh-checkpoints"

opt = requests.get(url=f"{url}/sdapi/v1/options")
opt_json = opt.json()
print("opt_json x ", opt_json)

opt_json["sd_model_checkpoint"] = "ICBINP.safetensors [9d0f63e649]"
requests.post(url=f"{url}/sdapi/v1/options", json=opt_json)

response = requests.get(url=f"{url}/sdapi/v1/sd-models")

print(response.json())
