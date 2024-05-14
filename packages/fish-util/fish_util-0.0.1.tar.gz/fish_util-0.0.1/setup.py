from setuptools import setup, find_packages

packages = find_packages()
print(packages)

setup(
    name="fish_util",
    version="0.0.1",
    packages=packages,
    description="Fishyer's Python Util Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="fishyer",
    author_email="yutianran666@gamil.com",
    url="https://github.com/fishyer/fish_util",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
