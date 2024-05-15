from setuptools import setup, find_packages

setup(
    name='osmtoroadgraph',
    version='0.1',
    packages=find_packages(include = ['osmtoroadgraph']),
    install_requires=[
        'networkx',
    ],
    python_requires='>=3.7',
    description='With this tool, osm data can be converted into easily parsable plaintext files that can be used by any application for further processing.',
    license='MIT',
    url='https://github.com/Crowley-VS/OsmToRoadGraph'
)
