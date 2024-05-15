import aonet.aonet as aonet

api_key = "4oipB83LZCpkrVN3i12f38WcBUYH5MR9"

aonet_instance = aonet.AON(api_key)

data = {
    "input":{
        "seed": 36446545872,
        "width": 768,
        "height": 768,
        "prompt": "with smoke, half ice and half fire and ultra realistic in detail.wolf, typography, dark fantasy, wildlife photography, vibrant, cinematic and on a black background",
        "scheduler": "K_EULER",
        "num_outputs": 1,
        "guidance_scale": 9,
        "negative_prompt": "scary, cartoon, painting",
        "num_inference_steps": 25
    }
}

result = aonet_instance.prediction("/predictions/ai/ssd-1b",data)

print(result)
