# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpt4o']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'gpt4o',
    'version': '0.0.1',
    'description': 'gpt4o - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# GPT4o\nCommunity Open Source Implementation of GPT4o in PyTorch\n\n\n## Install\n\n\n# Architecture\n- TikToken Tokenzier: We know fursure the tokenizer. [Which is here](https://github.com/openai/tiktoken)\n- Model understands Images and Audio Natively. There are 2 approaches, process them natively or use encoders for each. I think here they're using encoders like whisper and vit for simplicity and brevity.\n- Using DALLE3 as the output head to generate images\n- Tokens to denote when to generate an image or audio\n- Whisper output head for the audio outputs\n- \n\n# License\nMIT\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/gpt4o',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
