from setuptools import setup, find_packages

setup(
    name='jasyllablesep',
    version='0.0.0',
    packages=find_packages(),
    author='shimajiroxyza',
    author_email='shimaya.jiro@irl.sys.es.osaka-u.ac.jp',
    description='A package for separating Japanese text into syllables',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jiroshimaya/jasyllablesep',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
