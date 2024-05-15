# winter_rb_models
WINTER real/bogus ML models, originally created by [@aswinsuresh](https://github.com/aswinsuresh24)

This slimmed-down version uses pytorch rather than tensorflow.

[![PyPI version](https://badge.fury.io/py/winterrb.svg)](https://badge.fury.io/py/winterrb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installing the package

### Using pip

```bash
pip install winterrb
```

### From source

* Clone the repository
```bash
git clone git@github.com:winter-telescope/winterrb.git
```

* Navigate to the repository
```bash
cd winterrb
```

* Create a conda environment with the required packages
```bash
conda create -n winterrb python=3.11
```

* Activate the environment
```bash
conda activate winterrb
```

* Install the package
```bash
pip install -e .
```

## Training a model

You need a data directory, containing a list of training classifications in csv format, 
named `training_data.csv`, and a data containing the corresponding avro alerts used for training.
Specifically, you require a directory within the data directory named `train_data` containing the avro alerts.
Each avro alert should be named with the format `<id>.avro`.

You can set the data directory using the bash environment variable `WINTERRB_DATA_DIR`.

```bash
export WINTERRB_DATA_DIR=/path/to/data
```

Then you can train a model using the notebook `winterdrb_pytorch.ipynb`.
