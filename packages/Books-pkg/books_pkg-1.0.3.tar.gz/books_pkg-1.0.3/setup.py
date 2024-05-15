from setuptools import setup, find_packages

setup(

   name='Books_pkg',
   version='1.0.3',
   author='Milton Alejandro Angel Cardenas ',
   author_email='milton_ac@tesch.edu.mx',
   description='Es una libreria en la cual podremos encontrar el autor y el libro, de pende el que se escriba',
   packages= ['Books_pkg'],
   package_data={'Books_pkg': ['books.csv']},
   install_requires=['pandas',
                     'twine',
                     'wheel' ,
                     'setuptools'
                     ],
)


