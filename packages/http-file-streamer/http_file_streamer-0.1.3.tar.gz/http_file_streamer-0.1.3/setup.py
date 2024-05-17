from setuptools import setup, find_packages

setup(
    name="http_file_streamer",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
    ],
    author="Babak Zarrinbal",
    author_email="babak.zarrinbal@gmail.com",
    description="A package for streaming and receiving files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/babakzarrinbal/httpfilestreamer.git",  # Update with your actual repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
