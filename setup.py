from setuptools import setup

setup(
    name='cozer',
    version='0.1',
    py_modules=['cozer'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cozer=cozer:cli
    ''',
)