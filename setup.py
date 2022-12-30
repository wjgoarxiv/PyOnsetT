from setuptools import setup

setup(
	  name='PyOnsetT', 
	  version='1.0.6',  
	  description='::A simple onset temperature extractor for gas hydrate researchers::',
	  long_description= 'Revised some minor errors...', 
	  author='wjgoarxiv',
	  author_email='woo_go@yahoo.com',
	  url='https://pypi.org/project/PyOnsetT/',
	  license='MIT',
	  py_modules=['PyOnsetT'],
	  python_requires='>=3.8', #python version required
	  install_requires = [
	  'pandas',
	  'numpy',
	  'matplotlib',
	  'ruptures',
	  'tabulate',
	  'pyfiglet',
	  'argparse'
	  ],
	  packages=['PyOnsetT'],
		entry_points={
			'console_scripts': [
				'pyonsett = PyOnsetT.__main__:main'
			]
		}
	)
