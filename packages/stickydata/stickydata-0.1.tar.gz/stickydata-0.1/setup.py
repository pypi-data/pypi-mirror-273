from setuptools import setup, find_packages

setup(
    name='stickydata',
    version='0.1',
    packages=find_packages(),
    install_requires=[
       'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'numba'
    ],
    author='Demetrios Pagonis',
    author_email='demetriospagonis@weber.edu',
    description='package for correcting partitioning delays using deconvolution',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dpagonis/stickydata',
)
