from setuptools import setup

setup(
    name='blup',
    version='1.1',
    description='Turn JSON into HTML using Jinja',
    author='César Pichon',
    url='https://github.com/16arpi/blup',
    license='GPL-3.0',
    packages=['blup'],
    install_requires=['jinja2'],
    readme='README.md',
    entry_points={"console_scripts": ["blup=blup.__main__:main"]}
)
