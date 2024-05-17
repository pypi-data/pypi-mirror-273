from setuptools import setup, find_packages

setup(
    name="badger-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'badger=badger.cli:main',
        ],
    },
    author="Your Name",
    author_email="chris.kellet@bdgr.co.uk",
    description="A CLI for Badger Commerce",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Badger-Commerce/badger-cli",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
