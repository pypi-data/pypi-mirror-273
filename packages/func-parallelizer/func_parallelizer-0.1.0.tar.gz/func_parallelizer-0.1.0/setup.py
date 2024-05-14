from setuptools import setup, find_packages

setup(
    name='func_parallelizer',
    version='0.1.0',
    author='Vikash G',
    author_email='vikashgraja@gmail.com',
    description="Func_Parallelizer is a simple Python module for parallel execution of functions "
                "using multiprocessing. Ideal for parallel execution of heavy cpu operations",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=False
)
