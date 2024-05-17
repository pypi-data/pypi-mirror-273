from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='linkedin_user_scrape',
    version='1.0.6',
    author='Harika B V',
    author_email='harikabv.dev@gmail.com',
    description='LinkedIn scraper to parse user profiles',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    install_requires=[
        'selenium',
        'beautifulsoup4'
    ],
    python_requires='>=3.6',
    project_urls = {
        'Home page' : 'https://github.com/Harika-BV/LinkedIn-User-Scraper',
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)