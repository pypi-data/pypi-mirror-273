from setuptools import setup

setup(
    name='gmlutil-data-extraction',
    version='1.0.4',    
    description='General Machine Learning Utility Package for Data Extraction',
    url='https://github.com/Phillip1982/gmlutil_data_extraction',
    author='Phillip Kim',
    author_email='phillip.kim@ejgallo.com',
    license='BSD 2-clause', ## Change this
    packages=['gmlutil_data_extraction'],
    install_requires=[ # package>=0.2,<0.3
    	'aiobotocore==2.5.0',
    	'awscli==1.27.76',
		'boto3==1.26.76', # 1.20.24', 
		'botocore==1.29.76', # 1.23.24',
		'fuzzywuzzy>=0.18.0',
		'geopandas>=0.10.2',
        'hana-ml',
		'numpy>=1.19.5,<1.23.0',
        'oracledb>=1.4.2',
		'pandas>=1.3.5,<1.4.3',
		'psycopg2-binary>=2.9.1',
        'pymssql>=2.2.1',
        'python-levenshtein-wheels>=0.13.1',
		'pytrends>=4.7.3',
        'redshift_connector>=2.0.916',
		'sqlalchemy-redshift>=0.8.6'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS',
		'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
