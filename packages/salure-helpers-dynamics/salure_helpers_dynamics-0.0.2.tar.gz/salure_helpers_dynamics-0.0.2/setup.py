from setuptools import setup


setup(
    name='salure_helpers_dynamics',
    version='0.0.2',
    description='Datev wrapper from Dynamics365',
    long_description='Dynamics365 wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.dynamics"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
    ],
    zip_safe=False,
)