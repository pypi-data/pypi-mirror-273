from setuptools import setup, find_packages

setup(
    name='fazah',
    version='3.30',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aiden Lang, Will Foster',
    author_email='ajlang5@wisc.edu, wjfoster2@wisc.edu',
    packages=find_packages(),
    install_requires=[
        'deep_translator',
        'langdetect'
    ],
)
