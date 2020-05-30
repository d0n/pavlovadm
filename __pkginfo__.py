"""pavlovadm packaging information"""
name = 'pavlovadm'
provides = ['pavloavadm']
version = '0.1'
install_requires = [
    'requests', 'inquirer', 'cmd', 'PyYAML']
url = 'https://github.com/d0n/pavlovadm'
license = "GPLv3+"
author = 'd0n'
description = 'utility to manage pavlov\'s rcon like admin interface'
author_email = 'mail@leonpelzer.de'
classifiers = ['Environment :: Console',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'License :: OSI Approved :: ' \
                   'GNU General Public License v3 or later (GPLv3+)',
               'Programming Language :: Python :: 3',
               'Topic :: Desktop Environment',
               'Topic :: Utilities',
               'Topic :: Games']
include_package_data = True
long_description = ''

entry_points = {
    'console_scripts': ['pavlovadm = pavlovadm.pavlovadm:cli']}

package_data = {
    '': ['pavlovadm/example']}
