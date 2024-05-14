from setuptools import setup, find_packages

setup(

   name='Books_Lib',
   version='1.0.9',
   author= 'Milton Alejandro Angel Cardenas ',
   author_email='milton_ac@tesch.edu.mx',
   description='Es una libreria en la cual podremos encontrar el autor y el libro, de pende el que se escriba',
   packages= ['Books_Lib'],
   package_data={'Books_Lib': ['books.csv']},
   install_requires=['pandas',
                     'twine',
                     'wheel' ,
                     'setuptools'
                     ],
)
