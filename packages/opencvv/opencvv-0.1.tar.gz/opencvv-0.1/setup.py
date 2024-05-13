from setuptools import setup, find_packages

setup(
    name='opencvv',
    version='0.1',
    packages=find_packages(),
    package_data={'opencvv': ['data/*']},
    include_package_data=True,
    description='Code for IPCV',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='cockroachwater42',
    author_email='cockroachwater42@gmail.com',
    url='https://github.com/',
)