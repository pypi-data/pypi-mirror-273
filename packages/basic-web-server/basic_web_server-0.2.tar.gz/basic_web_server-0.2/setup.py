from setuptools import setup, find_packages

setup(
    name='basic-web-server',
    version='0.2',
    description='A basic web server that can render HTML or plain text.',
    author='kaimv',
    author_email='kaimv.hi@gmail.com',
    url='https://github.com/kaimv/basic-webserver',
    packages=find_packages(),
    py_modules=['basic_webserver'],
)
