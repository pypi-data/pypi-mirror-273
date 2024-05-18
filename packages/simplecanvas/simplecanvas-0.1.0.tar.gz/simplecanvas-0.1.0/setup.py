from setuptools import setup, find_packages

setup(
    name='simplecanvas',
    version='0.1.0',
    author='Piotr Żarczyński',
    author_email='piotr.zarczynski.06@gmail.com',
    description='A package that allows you to create a simple input canvas.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)