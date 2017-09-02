from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='cachelper',
    version='0.2.0',
    description='A collection of cache helpers',
    long_description=long_description,
    url='https://github.com/suzaku/cachelper',
    license='MIT',
    author='Satoru Logic',
    author_email='satorulogic@gmail.com',
    packages=['cachelper'],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cache',
)
