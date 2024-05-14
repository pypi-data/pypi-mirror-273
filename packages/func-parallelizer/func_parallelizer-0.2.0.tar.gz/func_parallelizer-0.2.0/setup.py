from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='func_parallelizer',
    version='0.2.0',
    author='Vikash G',
    author_email='vikashgraja@gmail.com',
    description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False
)
