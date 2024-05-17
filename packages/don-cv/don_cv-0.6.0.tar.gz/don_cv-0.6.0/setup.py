
from setuptools import setup, find_packages

setup(
        name="don-cv",
        version="0.6.0",
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'don-cv=don_cv.cli:main',
            ],
        },
        install_requires=[
            'rich',
            'PyYAML',
        ],
        author="Don Johnson",
        author_email="dj@codetestcode.io",
        description="A terminal GUI displaying a configurable resume",
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url="https://github.com/copyleftdev/don",
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
    )
    