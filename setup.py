import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-sprites",
    version = "0.4.0",
    author = "John Fink",
    author_email = "johnfink8@gmail.com",
    description = ("Django app models to handle image sprites to speed up page loads that have multiple small images."),
    license = "MIT",
    keywords = "django sprite image",
    url = "https://github.com/johnfink8/django-sprites",
    packages = ['sprites'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    ],
    install_requires=[
        'PIL',
        'uuid',
        'django',
        'urllib2',
        'urlparse',
    ]
)
