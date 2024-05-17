from setuptools import find_packages, setup

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("onnxstudio/version.py", "w") as f:
    f.write(f'__version__ = "{version}"\n')

setup(
    name="onnxstudio",
    version=version,
    description="OnnxStudio: Conveys a comprehensive suite of tools for working with ONNX models.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/inisis/OnnxStudio",
    author="inisis",
    author_email="desmond.yao@buaa.edu.cn",
    project_urls={
        "Bug Tracker": "https://github.com/inisis/OnnxStudio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    license="MIT",
    install_requires=[],
    packages=find_packages(exclude=("tests", "tests.*")),
    zip_safe=True,
    python_requires=">=3.6",
)