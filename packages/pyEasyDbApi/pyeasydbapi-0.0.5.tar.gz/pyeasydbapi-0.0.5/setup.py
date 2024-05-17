from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='pyEasyDbApi',
    version='0.0.5',
    author='n1grtr33x',
    author_email='dmitroluc7@gmail.com',
    description='Simple DataBase to use',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://t.me/n1grtr33x',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='easy-db',
    project_urls={
    },
    python_requires='>=3.7'
)
