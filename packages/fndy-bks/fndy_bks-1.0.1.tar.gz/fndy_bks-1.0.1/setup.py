from setuptools import setup, find_packages

setup(

   name='fndy_bks',
   version='1.0.1',
   author='Missael Angel Cardenas ',
   author_email='missael_ac@tesch.edu.mx',
   description='Es una libreria en la cual podremos encontrar el autor y el nombre '
               'del libro que queremos, de pende el que se escriba',
   packages= ['fndy_bks'],
   package_data={'fndy_bks': ['books.csv']},
   install_requires=['pandas', 'twine', 'wheel', 'setuptools'
                     ],
)
