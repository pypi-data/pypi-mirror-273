from setuptools import setup, find_packages


setup(
    name='satsure-core-test',
    version='0.2.6',
    description='satsure core package',
    author='Satsure',
    author_email='kmstpm@email.com',
    packages=find_packages(),
    install_requires=['awscli', 'fiona','gdal==3.6.2', 'google-cloud-storage', 'pandas',
                      'pyproj', 'pystac','pystac-client', 'python-dotenv', 'rasterstats',
                      'rasterio', 'requests', 'requests', 'sqlalchemy', 'wget'],
    include_package_data=True,
    package_data={
        'satsure-core-test': ['satelite/*.json'],
    }
)
