from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='remlaversionutilpy',
    use_scm_version={'local_scheme': lambda version: '',},
    setup_requires=['setuptools_scm'],

    packages=find_packages(),
    install_requires=required_packages
)
