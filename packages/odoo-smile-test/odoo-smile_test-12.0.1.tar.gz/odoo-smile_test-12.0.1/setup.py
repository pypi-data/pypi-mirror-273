from distutils.core import setup
from setuptools import find_packages


setup(
    name='odoo-smile_test',
    version='12.0.1',
    packages=find_packages(),
    data_files=[
        'smile_test/.coveragerc',
    ],
    include_package_data=True,
    license='LGPL',
    description='Smile test module',
    author='Smile',
    author_email='martin.deconinck@smile.fr',
    keywords=['odoo', 'test', 'smile_test', 'smile'],
    install_requires=[
        'coverage',
        'flake8',
        'unittest2',
        'xmlrunner',
        'debugpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
