#!/usr/bin/env python
# This file is part account_es module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from setuptools import setup
import re
import os
import io
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

MODULE = 'account_bank_statement_create_transactions'
PREFIX = 'trytoncalidae'
MODULE2PREFIX = {
    # 'account_bank_statement_account': 'trytonspain',
    # 'analytic_bank_statement': 'nantic',
}


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (
        name, major_version, minor_version,
        major_version, minor_version + 1
    )
    return require


config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

# requires = [
    # 'trytonspain_account_bank_statement @ '
    # 'https://github.com/trytonspain/trytond-account_bank_statement/'
    # 'archive/refs/heads/5.2.zip#'
    # 'egg=trytonspain_account_bank_statement<5.3',
    # 'trytonspain_account_bank_statement_account @ '
    # 'https://github.com/trytonspain/trytond-account_bank_statement_account/'
    # 'archive/refs/heads/5.2.zip#'
    # 'egg=trytonspain_account_bank_statement_account<5.3',
    # 'trytonspain_account_move_draft @ '
    # 'https://github.com/trytonspain/trytond-account_move_draft/'
    # 'archive/refs/heads/5.2.zip#'
    # 'egg=trytonspain_account_move_draft<5.3',
    # 'nantic_analytic_bank_statement @ '
    # 'https://github.com/NaN-tic/trytond-analytic_bank_statement/'
    # 'archive/refs/heads/5.2.zip#'
    # 'egg=nantic_analytic_bank_statement<5.3',
# ]
requires = []

for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('%s_%s' % (prefix, dep)))
requires.append(get_require_version('trytond'))

tests_require = [
    'factory_trytond',
]
# dependency_links = [
#     'https://github.com/NaN-tic/trytond-analytic_bank_statement/'
#     'archive/refs/heads/5.2.zip',
#     'https://github.com/trytonspain/trytond-account_bank_statement_account/'
#     'archive/refs/heads/5.2.zip',
# ]
series = '%s.%s' % (major_version, minor_version)
if minor_version % 2:
    branch = 'master'
else:
    branch = series

dependency_links = [
    'git+https://github.com/trytonspain/'
    f'trytond-account_bank_statement_account@{branch}'
    f'#egg=trytonspain_account_bank_statement_account',
    'git+https://github.com/NaN-tic/'
    f'trytond-analytic_bank_statement@{branch}'
    f'#egg=trytonspain_analytic_bank_statement',
]

if minor_version % 2:
    # Add development index for testing with proteus
    dependency_links.append('https://trydevpi.tryton.org/')

setup(
    name='%s_%s' % (PREFIX, MODULE),
    version=version,
    description='Create multiple transactions from bank statement line',
    long_description=read('README.md'),
    author='Calidae',
    author_email='dev@calidae.com',
    url="https://github.com/calidae/%s" % MODULE,
    download_url=" https://pypi.org/projects/trytoncalidae-%s" % MODULE,
    keywords='',
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
        'trytond.modules.%s.tests.factories' % MODULE,  # FIXME
        ],
    package_data={
        'trytond.modules.%s' % MODULE: (
            info.get('xml', [])
            + [
                'tryton.cfg',
                'view/*.xml',
            ]
        ),
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Catalan',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    use_2to3=True,
)
