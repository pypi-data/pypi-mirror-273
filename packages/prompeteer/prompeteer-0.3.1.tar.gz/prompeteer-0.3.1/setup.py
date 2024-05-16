from setuptools import setup, find_packages

# Read the contents of your README file
with open("public_README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='prompeteer',
    version='0.3.1',
    author='Yoaz Menda',
    author_email='yoazmenda@gmail.com',
    description='Prompt Development and Evaluation tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests', 'tests.*', 'README.md']),  # Include all packages
    py_modules=['prompeteer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml',
        'openai == 1.28.1',
        'azure-identity',
        'boto3',
        'tenacity'
    ],
)
