from setuptools import setup, find_packages

description = "Rapidly build GUI with Python and Qt"
setup(
    name = "simplewidgets",
    version = "0.1",
    packages = ['simplewidgets', 'simplewidgets.tests'],
    
    # metadata for upload to PyPI
    author = "Igor Tibes Ghisi",
    author_email = "itghisi@gmail.com",
    description = description,
    license = "LGPL",
    keywords = "qt",
    url = "http://github.com/itghisi/simplewidgets",  
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: User Interfaces',
    ]
)
