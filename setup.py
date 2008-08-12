from distutils.core import setup

# Dynamically calculate the version based on ink.VERSION.
version_tuple = __import__('ink').VERSION
if version_tuple[2] is not None:
    version = '%d.%d_%s' % version_tuple
else:
    version = '%d.%d' % version_tuple[:2]

setup(
    name = 'ink',
    version = version,
    description = 'Blogging application for Django',
    author = 'Jon Parise',
    author_email = 'jon@indelible.org',
    url = 'http://www.indelible.org/projects/ink/',
    packages = ['ink', 'ink.templatetags'],
    classifiers = ['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content'],
)
