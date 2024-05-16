from setuptools import setup, find_packages

VERSION = '1.0.0' 
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
        # package_dir={'': 'src'},
        package_data={'': ['*.pyd','*.so','__pycache__/*.pyc','.dylibs/*.dylib','../psycopg2_binary.libs/*.*']},
        include_package_data=True,
        install_requires=[], # add any additional packages that 
        # extras_require={'test': ['pytest', 'pytest-watch']},
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