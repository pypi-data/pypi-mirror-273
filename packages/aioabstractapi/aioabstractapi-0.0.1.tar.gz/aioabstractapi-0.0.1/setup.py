from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()
    
setup(
    name='aioabstractapi',
    version='0.0.1',
    author='Immortal',
    author_email='pavelmarklev507@gmail.com',
    description='abstractapi.com asynchronous python wrapper',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ImmortalNameless/aioabstractapi',
    packages=find_packages(),
    install_requires=['aiohttp==3.8.3', 'certifi==2023.5.7', 'strenum==0.4.10', 'pydantic==2.4.1'],
    license='MIT',
    keywords=[
        'abstract',
        'aioabstract',
        'abstract api',
        'aioabstract api'
    ],
    project_urls={
        'GitHub': 'https://github.com/ImmortalNameless'
    },
    python_requires='>=3.8'
)