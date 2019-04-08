from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='nexo-api-logs',
    version='1.0.0',
    description='Rest Api to get the log traces of the local filesystem.',
    long_description=readme,
    author='Angel Rojo',
    author_email='angel.rojo.perez@gmail.com',
    url='https://github/ilittleangel/nexo-api-logs.git',
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'flask_restful']
)
