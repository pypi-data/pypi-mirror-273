from setuptools import setup, find_packages

setup(
    name='cnl2asp-test',
    version='1.0.3',
    description='Hello',
    long_description='World',
    url='https://github.com/simocaruso/test',
    license='Apache License',
    author='Simone Caruso',
    author_email='simone.caruso@edu.unige.it',
    maintainer='Simone Caruso',
    maintainer_email='simone.caruso@edu.unige.it',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests*']),
    entry_points={
        'console_scripts': ['printer = printer.main:main'],
    },
    python_requires=">=3.10"
)