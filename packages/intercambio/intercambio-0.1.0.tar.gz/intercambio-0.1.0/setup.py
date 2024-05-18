from setuptools import setup, find_packages


setup(
    name="intercambio",
    version="0.1.0",
    packages=find_packages(),
    description="Uma biblioteca de exemplo com classes para testes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Alisson",
    #author_email="seu_email@example.com",
   # url="https://github.com/seu_usuario/minhalib",
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    python_requires='>=3.6',
)