import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pithermalcam",
    version="0.9.17",
    author="Tom Shaffner",
    description="A package which connects an MLX90640 Thermal IR Camera to a Raspberry Pi for viewing or web streaming.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://tomshaffner.github.io/PiThermalCam/",
    packages=['pithermalcam'],
    install_requires=[
        'numpy>=1.16.5',
        'matplotlib>=3.0.2',
        'scipy>=1.6.0',
        'RPI.GPIO>=0.7.0',
        'Adafruit-Blinka>=5.13.1',
        'adafruit-circuitpython-mlx90640>=1.2.1',
        'flask>=1.0.2',
        'opencv-python>=4.5.1.48',
        'cmapy>=0.6.6',
      ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/ or https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="raspberry pi mlx90640 thermal camera ir flir",
    python_requires='>=3.6',
    setup_requires=[
        "flake8"
    ],
    include_package_data=True,
    # What does your project relate to?
)
