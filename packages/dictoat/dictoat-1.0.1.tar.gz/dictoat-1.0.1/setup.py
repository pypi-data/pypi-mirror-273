from setuptools import setup, find_packages

setup(
    name='dictoat',
    version='1.0.1',
    packages=find_packages(),
    description='Convert a dict into an object to access items faster.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/niCodeLine/dictoat',
    author='Nico Spok',
    author_email='nicospok@hotmail.com',
    license='MIT',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)