from setuptools import setup

"""
Fixtures folder has been included in Manifest.in file.
https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
https://docs.python.org/2/distutils/sourcedist.html#principle
"""

setup(
    name='onestop_opensign',
    version='0.1.6.1',
    author='OTB Africa',
    author_email='developers@otbafrica.com',
    license='BSD 2-clause',
    description='Package for a onestop extension that integrates with the opensign digital signature service.',
    packages=[
        'onestop_opensign',
        'onestop_opensign.migrations'
    ],
    include_package_data=True, # Include files from MANIFEST.in e.g. fixtures
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'django',
        'django-fsm'
    ],
)