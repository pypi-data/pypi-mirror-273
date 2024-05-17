from setuptools import setup, find_packages

setup(
    name='bridger',
    version='0.0.1_dev',
    author='Matt Durrant',
    author_email='matthew@arcinstitute.org',
    description='bridger',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hsulab-arc/Bridger',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)