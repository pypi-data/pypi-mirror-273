from setuptools import setup


setup(name='VioleRCNG',
    version='0.0.1',
    license='MIT License',
    author='Jorge Magno',
    long_description="Viole is a Python library that generates random code names using a combination of letters and numbers. It provides flexibility in generating code names with different patterns and components.",
    long_description_content_type="text/markdown",
    author_email='jorge.estudos0@gmail.com',
    keywords='code, name generator',
    description=u'A random code name generator for anything',
    packages=['viole_rcng'],
    install_requires=['random', 'string'],)