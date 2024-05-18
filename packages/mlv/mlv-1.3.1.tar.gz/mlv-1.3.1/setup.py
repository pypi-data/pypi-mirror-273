from setuptools import find_packages, setup

setup(
    name="mlv",
    version="1.3.1",
    install_requires=[
        "diffusersv",
        "torch==2.2.2",
        "transformers==4.39.2",
        "accelerate==0.28.0",
        "pillow==10.2.0",
        "omegaconf==2.3.0",
        "safetensors==0.4.2",
        "peft==0.10.0",
    ],
    packages=find_packages("."),
    python_requires=">=3.10",
)
