import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pithermalcam",
    version="0.0.1",
    author="Tom Shaffner",
    author_email="tom.shaffner@yahoo.com",
    description="A package which connects an MLX90640 Thermal IR Camera to a Raspberry Pi for viewing or web streaming.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tomshaffner.github.io/PiThermalCam/",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
        'scipy'
        'RPI.GPIO'
        'Adafruit-Blinka'
        'adafruit-circuitpython-mlx90640'
        'flask'
        'opencv-contrib-python'
        'cmapy'
      ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/ or https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)