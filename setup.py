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
    version = "0.2.0",
    author = "John Fink",
    author_email = "johnfink8@gmail.com",
    description = ("Django app models to handle image sprites to speed up page loads with multiple small images."),
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
        "Topic :: Internet :: WWW/HTTP :: WSGI"
    ],
    install_requires=[
        'PIL',
        'uuid',
        'django',
    ]
)
