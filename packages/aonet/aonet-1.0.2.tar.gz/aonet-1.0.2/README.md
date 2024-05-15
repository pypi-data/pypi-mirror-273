# AON

AON - Python sdk for AON
A Python lib for AON. It lets you run models from your Python code, and everything else you can do with AON HTTP API.

- API version: 1.0
- Package version: 1.0.0

## Installation

### For [Python](https://www.python.org/)

#### npm

Install it from pip:

```shell
pip install aonet
```

## Getting Started

Please follow the [installation](#installation) instruction and execute the following JS code:

```python
from aonet import aonet

#get your api key or jwt token from https://console.aonet.ai
api_key = "my api key or jwt token"

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

```

## API

All URIs are relative to *https://api.aonet.ai*

### Constructor

```javascript
aonet_instance = aonet.AON(auth,host,headers)
```

name | type | Description
------------ | ------------- | -------------
*host* | string | The request host
*auth* | string | **Required**.You can choose either API key or JWT token for authentication.


## Docs

For more information, please visit the site *https://docs.aonet.ai*