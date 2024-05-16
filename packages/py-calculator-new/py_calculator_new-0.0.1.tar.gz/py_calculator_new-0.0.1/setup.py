from setuptools import setup, find_packages

setup(
    name="py_calculator_new",
    version="0.0.1",
    author="Vinayak Gaikar",
    author_email="vinayakgaikar1998@gmail.co,",
    description="An application that peforme simple calculaltion like calculator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #install_requires=["pandas"],
    entry_points={"console_scripts": ["py_calculator_new = src.main:main"]},
)

