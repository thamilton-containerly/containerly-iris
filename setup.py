import setuptools

setuptools.setup(
    name="containerly-runtime",
    version="0.1.0",
    author="containerly.io@gmail.com",
    author_email="containerly.io@gmail.com",
    description="containerly-runtime",
    url="https://github.com/containerly-runtime",
    packages=setuptools.find_packages(exclude=[]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "containerly-runtime = runtime.cli:cli"
        ]
    },
    install_requires=[
        "click",
        "protobuf"
    ],
    python_requires=">=3.7.3"
)