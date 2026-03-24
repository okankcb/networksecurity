"""
Le fichier setup.py est une partie essentielle du packaging 
et de la distribution des projets Python. Il est utilisé par setuptools 
(ou distutils dans les anciennes versions de Python) pour définir 
la configuration de votre projet, comme ses métadonnées, ses dépendances, et plus encore.
"""

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requirements 
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt', 'r') as file:
            #Read lines frome the file
            lines = file.readlines()
            #Process each line 
            for line in lines:
                requirement = line.strip()
                #ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

print(get_requirements())

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author="okandata",
    author_email="contact@okandata.com",
    packages=find_packages(),
    install_requires=get_requirements()
)



