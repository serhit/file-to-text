from setuptools import setup

setup(
    name='file_to_text_converter',
    version='0.0.1',
    packages=['file_to_text'],
    url='https://github.com/serhit/file-to-text.git/',
    license='MIT',
    install_requires=['httpx>=0.21.1', 'aiofiles>=0.7.0'],
    author='Sergey Khitrin',
    author_email='serhit@gmail.com',
    description='API for FileToText service - online service to convert files of various types to plain text'
)
