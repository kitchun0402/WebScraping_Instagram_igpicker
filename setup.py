import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='igenemy',  
     version='0.2',
     scripts=['igenemy'] ,
     author="Kenneth Hau",
     author_email="kitchun0402@gmail.com",
     description="WebScraping_Instagram",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/kitchun0402/WebScraping_Instagram_igenemy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
