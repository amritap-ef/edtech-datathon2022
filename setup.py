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
        "streamlit==1.14.1",
        "streamlit-player==0.1.5"
        "transformers==4.24.0",
        "nltk==3.7"
        # "sentencepiece",
        "huggingface_hub==0.10.1",
        "elasticsearch==7.10",
        "pandas==1.5.1",
        "beautifulsoup4==4.11.1",
        "streamlit-option-menu==0.3.2",
        "openai==0.25.0"
    ],
    extras_require={
    },
)