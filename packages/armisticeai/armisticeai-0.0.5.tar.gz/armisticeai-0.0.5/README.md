# ArmisticeAI Python Library

The ArmisticeAI Python library provides convenient access to the ArmisticeAI API from applications written in Python. It includes a pre-defined set of classes for API resources that initialize themselves dynamically from API responses.

## Installation

Install the packages listed in `requirements.txt`:

```bash
$ pip install torch torchvision transformers accelerate evaluate datasets peft scikit-learn flwr huggingface-hub peft
$ pip install git+https://github.com/tanyav2/bitsandbytes.git@tanya/lora-fix#egg=bitsandbytes
```

Then run:
```bash
$ pip install --upgrade armisticeai
```
which installs the latest version of the package.

If you want to modify the package, you need to install from source. In order to do so, you will need to use `maturin` which builds the Rust components of this package:

```bash
$ pip install maturin patchelf
$ maturin develop --release
```

## Usage

TODO

### Set up Admin

```python
from armisticeai import Admin

admin = Admin(access_code="test-code", task="image-classification")

project_id = admin.create_project()

training_config = admin.create_training_config()
```

### Set up Clients

```python
from armisticeai import Client

client = Client(project_id='')

training_config = client.get_training_config()

client.train()
```

### Full training run


