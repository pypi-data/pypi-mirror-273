from setuptools import setup, find_packages
from os import path

name = "video-representations-extractor"
version = "1.0.1"
description = "Video Representations Extractor (VRE) for computing algorithmic or neural representations of each frame."
url = "https://gitlab.com/meehai/video-representations-extractor"

loc = path.abspath(path.dirname(__file__))
with open(f"{loc}/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required = ["numpy>=1.21.6", "PyYAML==6.0", "argparse==1.1", "pims==0.6.1", "tqdm==4.66.1", "scikit-image==0.19.3",
            "natsort==8.2.0", "gitpython==3.1.31", "gdown==4.6.0", "torch==2.1.0", "torchvision==0.16.0",
            "timm==0.6.13", "transforms3d==0.4.1", "pyproj>=3.2.0", "overrides==7.3.1", "pandas==2.1.3",
            "matplotlib==3.7.1", "flow_vis==0.1", "colorama==0.4.6", "omegaconf==2.3.0", "lovely_tensors==0.1.15",
            "ultralytics==8.0.120", "fvcore==0.1.5.post20221221", "pycocotools==2.0.7", "cloudpickle==3.0.0"]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=find_packages(),
    install_requires=required,
    dependency_links=[],
    license="WTFPL",
    python_requires=">=3.9",
    scripts=["bin/vre"],
)
