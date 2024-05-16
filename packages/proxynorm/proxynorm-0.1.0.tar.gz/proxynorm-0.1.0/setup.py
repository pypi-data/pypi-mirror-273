from setuptools import setup, find_packages

setup(
    name="proxynorm",
    version="0.1.0",
    url="https://github.com/Khochawongwat/ProxyNorm-Pytorch",
    author="Khochawongwat Kongpana",
    author_email="khochawongwat.kongpana@gmail.com",
    description="Implementation of Proxy Normalization in PyTorch",
    packages=find_packages(),
    install_requires=["numpy", "torch", "scipy"],
)
