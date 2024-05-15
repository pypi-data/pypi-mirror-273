from setuptools import setup, find_packages

setup(
    name='screenshotpath',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'screenshotpath=screenshotpath.screenshotpath:main',
        ],
    },
    install_requires=[
        'argparse',
    ],
    author='Isa Bin Mohamed Yamin',
    author_email='boiwantlearncode@gmail.com',
    description='A package to change macOS screenshot path',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/boiwantlearncode/screenshotpath',
)
