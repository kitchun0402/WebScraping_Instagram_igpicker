from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='igpicker',  
    version='0.4.4',
    author="Kenneth Hau",
    author_email="kitchun0402@gmail.com",
    description="WebScraping_Instagram",
    url="https://github.com/kitchun0402/WebScraping_Instagram_igpicker",
    license = 'MIT',
    zip_safe = False,
    packages=['igpicker'],
    install_requires = ['selenium>=3.141.0', 'bs4>=0.0.1', 'ipython>=7.8.0', 'wget>=3.2', 'tqdm>=4.36.1'],
    python_requires = '>= 3',
    long_description=long_description,
    long_description_content_type="text/markdown"
 )
