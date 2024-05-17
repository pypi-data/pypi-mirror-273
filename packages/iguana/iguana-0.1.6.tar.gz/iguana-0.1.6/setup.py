from setuptools import setup, find_packages

setup(
    name='iguana',
    version='0.1.6',
    description='A network scanning tool for Kali Linux',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Uveis Smajli',
    author_email='smajliuveis@yahoo.com',
    url='https://pypi.org/project/iguana/',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'iguana=iguana:main',
        ],
    },
    install_requires=[
        'scapy',
        'dnspython',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
