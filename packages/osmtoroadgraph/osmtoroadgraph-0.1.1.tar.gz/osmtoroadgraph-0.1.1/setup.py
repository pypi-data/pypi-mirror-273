from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='osmtoroadgraph',
    version='0.1.1',
    packages=find_packages(include = ['osmtoroadgraph']),
    install_requires=[
        'networkx',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    description='With this tool, osm data can be converted into easily parsable plaintext files that can be used by any application for further processing.',
    license='MIT',
    url='https://github.com/Crowley-VS/OsmToRoadGraph'
)
