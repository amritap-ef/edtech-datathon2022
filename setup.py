from setuptools import find_packages, setup

setup(
    name="datathon-edtech2022",
    version="0.1",
    packages=find_packages(),
    url="http://www.ef.com",
    license="",
    author="",
    author_email="",
    description="Datathon ACR libraries",

    install_requires=[
        "streamlit",
        # "transformers[sentencepiece]",
        # "sentencepiece",
        "huggingface_hub",
        "elasticsearch==7.10"
    ],
    extras_require={
    },
)