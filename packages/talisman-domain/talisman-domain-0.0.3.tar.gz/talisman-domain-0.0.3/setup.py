from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", "r", encoding="utf-8") as f:
    version = f.read()

setup(
    name='talisman-domain',
    version=version,
    description='Talisman domain implementations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ISPRAS Talisman NLP team',
    author_email='modis@ispras.ru',
    maintainer='Vladimir Mayorov',
    maintainer_email='vmayorov@ispras.ru',
    packages=find_packages(include=['tie_domain', 'tie_domain.*']),
    install_requires=[
        'talisman-interfaces~=0.5.6', 'talisman-dm~=1.0.0a34',
        'aiohttp~=3.8.4', 'aiohttp-retry~=2.8.3', 'aiorwlock~=1.3.0',
        'fastapi>=0.73.0', 'pydantic~=1.10.4', 'gql~=3.4.0', 'graphql-core~=3.2.3',
        'requests~=2.31.0', 'python-keycloak~=2.16.2', 'typing_extensions~=4.8.0'

    ],
    entry_points={
        'talisman.plugins': ['domain = tie_domain']
    },
    data_files=[('', ['VERSION'])],
    python_requires='>=3.10',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License'
    ]
)
