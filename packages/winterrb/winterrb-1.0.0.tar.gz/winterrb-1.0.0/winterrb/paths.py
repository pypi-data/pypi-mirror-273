"""
Module for handling paths in the WinterRB project.
"""
import os
from pathlib import Path

data_dir = os.getenv("WINTERRB_DATA_DIR", None)
if data_dir is None:
    data_dir = Path.home().joinpath("Data/winter_real_bogus")

train_class_path = data_dir / "data_train.csv"

code_dir = Path(__file__).resolve().parent

model_dir = code_dir.parent / "models"
model_dir.mkdir(exist_ok=True)

