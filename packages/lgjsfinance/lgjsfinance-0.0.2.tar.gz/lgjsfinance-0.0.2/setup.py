from setuptools import setup

setup(
    name='lgjsfinance',
    version='0.0.2',    
    description='LGJS Finance',
    url='https://liamgenjs.vercel.app',
    author='liamgen.js',
    author_email='liamgen.js@proton.me',
    license='BSD 2-clause',
    packages=['lgjsfinance'],
    install_requires=['yfinance>=0.2.38',
                      'matplotlib',
                      'datetime',                
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)