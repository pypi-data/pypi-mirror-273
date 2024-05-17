from setuptools import setup, find_packages

setup(
    name='json24',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    description='A library to parse partial JSON strings with optional logging for faulty JSON.',
    author='Ali Argun Sayilgan',
    author_email='yeargun@stuf24.com',
    url='https://github.com/yeargun/json24-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
