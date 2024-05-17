# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vision_mamba']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'vision-mamba',
    'version': '0.0.6',
    'description': 'Vision Mamba - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Vision Mamba\nImplementation of Vision Mamba from the paper: "Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model" It\'s 2.8x faster than DeiT and saves 86.8% GPU memory when performing batch inference to extract features on high-res images. \n\n[PAPER LINK](https://arxiv.org/abs/2401.09417)\n\n## Installation\n\n```bash\npip install vision-mamba\n```\n\n# Usage\n```python\n\nimport torch\nfrom vision_mamba.model import Vim\n\n# Create a random tensor\nx = torch.randn(1, 3, 224, 224)\n\n# Create an instance of the Vim model\nmodel = Vim(\n    dim=256,  # Dimension of the model\n    heads=8,  # Number of attention heads\n    dt_rank=32,  # Rank of the dynamic routing tensor\n    dim_inner=256,  # Inner dimension of the model\n    d_state=256,  # State dimension of the model\n    num_classes=1000,  # Number of output classes\n    image_size=224,  # Size of the input image\n    patch_size=16,  # Size of the image patch\n    channels=3,  # Number of input channels\n    dropout=0.1,  # Dropout rate\n    depth=12,  # Depth of the model\n)\n\n# Perform a forward pass through the model\nout = model(x)\n\n# Print the shape and output of the forward pass\nprint(out.shape)\nprint(out)\n\n\n\n```\n\n\n\n## Citation\n```bibtex\n@misc{zhu2024vision,\n    title={Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model}, \n    author={Lianghui Zhu and Bencheng Liao and Qian Zhang and Xinlong Wang and Wenyu Liu and Xinggang Wang},\n    year={2024},\n    eprint={2401.09417},\n    archivePrefix={arXiv},\n    primaryClass={cs.CV}\n}\n```\n\n# License\nMIT\n\n\n# Todo\n- [ ] Fix the encoder block with the forward and backward convolutions\n- [ ] Make a training script for imagenet',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/VisionMamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
