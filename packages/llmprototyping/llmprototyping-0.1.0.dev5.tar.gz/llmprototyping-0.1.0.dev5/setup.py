from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="llmprototyping",
    # https://packaging.python.org/en/latest/discussions/versioning/
    version="0.1.0.dev5",
    description="A lightweight set of tools to use several llm and embeddings apis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alejandrolc/llmprototyping",
    author="Alejandro López Correa",
    #author_email="...",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="llm, rag, openai, groq, ollama",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    install_requires=required,
)