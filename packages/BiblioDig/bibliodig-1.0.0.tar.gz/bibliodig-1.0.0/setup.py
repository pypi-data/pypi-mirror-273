from setuptools import setup, find_packages

setup(
    name='BiblioDig',
    version='1.0.0',
    author='Luz Lizeth Vazquez Garcia',
    author_email='luzlizet35@gmail.com',
    description='Biblioteca que busque un libro ya sea por nombre, autor, año o alguna otra caracteristica',
    packages=["BiblioDig_Py"],
    package_data={'BiblioDig:Py': ['books.csv']},
    install_requires=[
        'pandas',
        'twine',
        'wheel',
        'setuptools',
    ],
)
