from setuptools import setup, find_packages

setup(
    name='sortipy',
    version='0.0.2',
    author='Bruno Peselli',
    author_email='brunopeselli@gmail.com',
    description='Sortipy is a Python package designed to simplify file organization within a directory.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pzzzl/sortipy',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
)
