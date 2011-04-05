import os
from distutils.core import setup

# also update version in __init__.py
version = '0.1'

setup(
    name="authlater",
    version=version,
    keywords=["django", "auth", "auth-later"],
    long_description=open(os.path.join(os.path.dirname(__file__),"README.md"), "r").read(),
    description="Authlater adds ability for non-authinticated users to post forms and only then login.",
    author="Anton Agafonov",
    author_email="equeny@gmail.com",
    url="http://github.com/equeny/authlater",
    license="Apache Software License",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=['authlater'],
    install_requires=['django>=1.2'],
    requires=['django (>=1.2)'],
    download_url="http://github.com/downloads/equeny/authlater/authlater-%s.tar.gz" % version,
)
