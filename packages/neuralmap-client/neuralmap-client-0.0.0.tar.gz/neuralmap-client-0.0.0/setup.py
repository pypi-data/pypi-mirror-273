from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'neuralmap-client',
    version = '0.0.0',
    description='Search and recommandation engines.',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://docs.neuralmap.io',
    author='Tensor AI',
    author_email='tensorai221@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    install_requires=['bson >= 0.5.10', 'aiohttp >= 3.9.5'],
    extras_require={
        'dev': ['pytest>=7.0', 'twine>=4.0.2'],
    },
    python_requires='>=3.10',
)