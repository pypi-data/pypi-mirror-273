from setuptools import setup, find_packages

setup(
    name='prompeteer',
    version='0.1.4',
    author='Yoaz Menda',
    author_email='yoazmenda@gmail.com',
    description='Prompt Development and Evaluation tool',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml',
        'openai == 1.28.1',
        'azure-identity'
    ],
)
