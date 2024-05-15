from setuptools import setup, find_packages

setup(
    name='shox',
    version='0.1.0',
    description='A powerful tool that combines the port-scanning and OSINT-gathering capabilities of shodan.io with the onhand downloadable exploits of ExploitDB.',
    author='Vadin02',
    url='https://gitlab.com/JIbald/shox',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flasgger',
        'click',
        'requests',
        'beautifulsoup4',
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'shox-api=api:main',
            'shox-cli=cli:call_api',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)