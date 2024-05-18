import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()


setup(
    name="django-exception-logger",
    version="0.1.3",
    packages=find_packages(exclude=["tests*"]),
    description="Adds error logging to the admin panel",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Titov Leonid",
    author_email="titov281@yandex.ru",
    url="https://github.com/Leonid-T/django-exception-logger/",
    license="MIT",
    install_requires=[
        "Django>=4.0",
    ],
)
