from setuptools import setup, find_packages


VERSION = '0.0.3'

setup(
    name='geotifflib',
    version=VERSION,
    author='flemyng feng',
    author_email='flemyng1999@outlook.com',
    description='A Python GeoTiff kit based on GDAL',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    keywords=['python', 'tiff', 'geotiff','windows','mac','linux'],
    url='https://github.com/Flemyng1999/geotifflib',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'geotifflib = geotifflib.main:main'
        ]
    }
)
