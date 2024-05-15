from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='basic-web-server',
    version='0.3',
    description='A basic web server that can render HTML or plain text.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='kaimv',
    author_email='kaimv.hi@gmail.com',
    url='https://github.com/kaimv/basic-webserver',
    packages=find_packages(),
    py_modules=['basic_webserver'],
)
