from setuptools import setup, find_packages

setup(
    name='randevu',
    version='2.0.0',
    author='TypicalHog',
    description='The official Python implementation of the RANDEVU algorithm',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TypicalHog/randevu-py',
    project_urls={
        'Homepage': 'https://github.com/TypicalHog/randevu-py',
        'Issues': 'https://github.com/TypicalHog/randevu-py/issues'
    },
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)
