from setuptools import setup, find_packages

setup(
    name='synochatbot',
    version='1.5',
    author='kokofixcomputers',
    description='A discord.py like thing but for synology chat',
    long_description_content_type='text/markdown',
    long_description='''
# A python library like discord.py but for synology chat.

It allows you to create a bot that can be used to respond to messages in synology chat.

## Install:
``pip install synochatbot``

## Usage:
```python
import synochatbot as synochat

import time
time.sleep(1)

outgoing_webhook = "your url"
instance = synochat.instance(prefix="?")

@instance.message(alias="hi")
def say_hi(message):
    return ('Hi!')

@instance.message(alias='return_test')
def return_test(message, command=None):
    return message.username

# ... (other message handlers)

synochat.run_bot(instance, outgoing_webhook, incomming_webhook_token)
```
    ''',
    packages=find_packages(),
    install_requires=[
        'flask==3.0.3',
        'requests==2.31.0'
    ],
)
