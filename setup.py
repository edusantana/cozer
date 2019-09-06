from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cozer',
    version='0.3',
    author="Eduardo de Santana Medeiros Alexandre",
    author_email="eduardo.ufpb@gmail.com",
    description="Um pequeno script para ensinar sobre como invocar comandos no terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edusantana/cozer",
    #packages=setuptools.find_packages(),
    py_modules=['cozer'],
    install_requires=[
        'Click','click_didyoumean'
    ],
    entry_points='''
        [console_scripts]
        cozer=cozer:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#    python_requires='>=3.4',
)
