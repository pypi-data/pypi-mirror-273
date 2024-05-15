from setuptools import setup, find_packages
setup(
    name='linkedin_user_scrape',
    version='1.0.1',
    author='Harika B V',
    author_email='harikabv.dev@gmail.com',
    description='LinkedIn scraper to parse user profiles',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)