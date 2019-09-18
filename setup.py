from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='igenemy',  
    version='0.2.1',
    author="Kenneth Hau",
    author_email="kitchun0402@gmail.com",
    description="WebScraping_Instagram",
    url="https://github.com/kitchun0402/WebScraping_Instagram_igenemy",
    license = 'MIT',
    zip_safe = False,
    packages=['igenemy'],
    dependency_links = ['https://pypi.org/project/selenium/', 'https://pypi.org/project/bs4/',
                        'https://pypi.org/project/ipython/'],
    python_requires = '>= 3',
    long_description=long_description,
    long_description_content_type="text/markdown"
 )
