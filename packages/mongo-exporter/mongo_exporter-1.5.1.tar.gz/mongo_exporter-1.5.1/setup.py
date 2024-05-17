from setuptools import setup

setup(
    name='mongo_exporter',
    version='1.5.1',
    description='A tool that supports exporting the database schema from MongoDB.',
    author='Alex Haimov',
    author_email='haimovalex@gmail.com',
    packages=['mongo_exporter'],
    install_requires=[
        "pymongo"
    ],
)