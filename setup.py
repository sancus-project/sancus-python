from distutils.core import setup

requires = [
    'webob',
    ]

setup(
    name='sancus',
    version='0.0dev',

    package_dir={'': 'src'},
    packages=['sancus',],

    install_requires = requires,
)
