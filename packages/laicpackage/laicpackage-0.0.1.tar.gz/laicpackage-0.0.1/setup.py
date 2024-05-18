# setup.py

from setuptools import setup, find_packages

setup(
    name="laicpackage",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Liste des dépendances si nécessaire
    entry_points={
        'console_scripts': [
            'monpackage=monpackage.info:afficher_nom_ascii',
        ],
    },
    author="Laic Maminiaina",
    author_email="maminiainalaic@gmail.com",
    description="Un package pour afficher le nom en ASCII et les informations de Laic Maminiaina",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tonutilisateur/monpackage",  # Remplacez par l'URL de votre projet si nécessaire
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

