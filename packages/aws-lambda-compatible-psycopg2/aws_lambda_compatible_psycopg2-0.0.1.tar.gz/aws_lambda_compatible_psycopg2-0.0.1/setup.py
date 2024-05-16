from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'PostgreSQL database adapter for the Python programming language.'
LONG_DESCRIPTION = 'PostgreSQL database adapter for the Python programming language.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="aws_lambda_compatible_psycopg2",
        version=VERSION,
        author="Abinaya Subba",
        author_email="abinaya.subba@anko.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            # "Development Status :: 4 - Beta",
            # "Intended Audience :: kmartau",
            # "Programming Language :: Python :: 3",
            # "Operating System :: MacOS :: MacOS X",
            # "Operating System :: Microsoft :: Windows",
        ]
)