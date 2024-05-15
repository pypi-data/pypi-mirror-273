import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    installation_requirements = fr.readlines()

setuptools.setup(
    name="moovs_business",
    version="0.0.1",
    author="Guilherme Viveiros, Rui Reis.",
    author_email="guilherme.viveiros@dotmoovs.com, rui.reis@dotmoovs.com",
    description="Empower your software with advanced object detection, human pose estimation, and real-time multi-object tracking to revolutionize how you interact with the physical world.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dotmoovs/moovs-business",
    packages=setuptools.find_packages(),
    install_requires=installation_requirements,
    python_requires=">=3.7",
)
