from setuptools import setup, find_packages

with open("README.md","r") as f:
    description = f.read()

setup(
    name='klazify',
    version='0.3',
    description = 'The most accurate Content Classification API. All-in-one domain data source',
    author = 'Klazify',
    author_email = 'hello@klazify.com',
    url = 'https://github.com/Zyla-Labs/pypi-klazify-api',
    keywords = ['Get Website Logos api','Brand Imagery api','We Categorize the Web', 'api for website', 'api key for website', 'logo api', 'banking logo api', 'company logo api',  'api key website', 'api of website',  'best api for website' , 'create an api for a website',  'create an api for your website', 'Website Category API' ,' Website Logo API' , 'logo api', 'URL logo api', 'Webshrinker',  'classifies a site into a category', 'brandfetch', 'url categorization', 'url category check api',  'website category lookup', 'web categories', 'url classification dataset'],
    packages=find_packages(),
    install_requires=[
        
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)