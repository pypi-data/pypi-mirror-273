import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ownotp',
    version='0.1.1',
    author='karthiksenniyappan',
    author_email='karthiksenniyappan76@gmail.com',
    description="Generate a time-based OTP using SHA-256 hashing algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karthiksenniyappan/ownotp",
    packages=['ownotp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
