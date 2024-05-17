from setuptools import setup, find_packages

setup(
    name='eurmlsdk',
    version='0.1.0',
    packages=find_packages(),
    description='eUR ML SDK',
    long_description=open('README.md').read(),
    install_requires=[
        'boto3',
        'numpy==1.24.3',
        'python-dotenv',
        'paramiko',
        'tensorflow==2.13.1',
        'tqdm',
        'ultralytics',
        'torch',
        'timm',
        'torchvision'
    ],
    author='eUR',
    author_email='aiml@embedur.com',
    license='MIT',
    entry_points={
        "console_scripts": [
            "eurmlsdk = eurmlsdk.__main__:main"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
