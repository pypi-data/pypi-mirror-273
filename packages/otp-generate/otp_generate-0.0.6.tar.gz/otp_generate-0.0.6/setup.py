from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='otp_generate',  # name of package which will be package dir below project
    version='0.0.6',
    url='https://github.com/MariMuthu15/otp-generate-package',
    author='Marimuthu',
    author_email='mahimari555@gmail.com',
    description='A simple otp generate package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    entry_points={
        'console_scripts': [
            'package-hello = otp_generate:package_check',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    python_requires='>=3',

)
