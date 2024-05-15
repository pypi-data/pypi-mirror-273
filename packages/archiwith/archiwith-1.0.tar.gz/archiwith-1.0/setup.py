from setuptools import setup, find_packages

setup(
    name='archiwith',
    version='1.0',
    packages=find_packages(),
    description='File opener and closener when managed via `with`.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/niCodeLine/archiwith',
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