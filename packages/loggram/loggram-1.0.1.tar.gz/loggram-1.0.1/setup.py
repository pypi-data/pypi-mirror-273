from setuptools import setup, find_packages

setup(
    name="loggram",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot'        
    ],
    author="Ilia Abolhasani",
    author_email="abolhasani.eliya@gmail.com",
    description="A package for sending logs to Telegram channels",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Ilia-Abolhasani/loggram",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)