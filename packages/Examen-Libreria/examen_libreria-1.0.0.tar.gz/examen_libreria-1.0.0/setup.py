from setuptools import setup, find_packages

setup(
    name='Examen_Libreria',
    packages=["Examen_Libreria"],
    version='1.0.0',
    install_requires=['pandas'],
    author='PABLO URIEL FRANCO CONTRERAS',
    author_email='202227011_franco@tesch.edu.mx',
    package_data={'Examen_Libreria': ['books_new.csv']},
    description='Proporciona una forma estructurada y eficiente de gestionar una colección de libros.',
)
