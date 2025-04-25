from setuptools import setup, find_packages

setup(
    name="Arriva",
    version="0.1",
    author="Nicolas Stillhard",
    description="Arriva is a Raspberry Pi-based system for displaying connections at a specified location.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author_email="nicolas.stillhard@gmail.com",
    url="https://github.com/nicoscore99/arriva",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        # Add your dependencies here
        # e.g. 'requests>=2.25.1',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
)

