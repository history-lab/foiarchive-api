from setuptools import setup, find_packages

setup(
    name='Declass API',
    version='2.0',
    long_description=__doc__,
    packages=find_packages(exclude=('tests', 'docs', 'env', 'config', 'data')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.12',
        'flask-cors>=3.0',
        'pyyaml>=3.12',
        'sqlalchemy>=1.2',
        'elasticsearch>=6.2',
        'requests>=2.18',
        'pymysql>=0.7'
    ]
)
