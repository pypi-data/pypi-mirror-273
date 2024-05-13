from setuptools import setup, find_packages

setup(
    name='satsure-core-test',
    version='0.0.7',
    description='satsure core package',
    author='Satsure',
    author_email='kmstpm@email.com',
    packages=find_packages(),
    install_requires=['awscli', 'fiona', 'google-cloud-storage', 'pandas',
                      'pyproj',
                      'pystac', 'python-dotenv', 'rasterstats', 'rasterio',
                      'requests',
                      'requests', 'sqlalchemy', 'wget']
)
