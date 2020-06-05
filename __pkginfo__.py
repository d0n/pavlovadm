"""pavlovadm packaging information"""
name = 'pavlovadm'
provides = ['pavloavadm']
version = '1.4'
install_requires = [
    'requests', 'inquirer', 'PyYAML']
url = 'https://pypi.org/project/pavlovadm/'
license = "GPLv3+"
author = 'd0n'
description = 'utility to issue commands to pavlov\'s rcon like admin interface'
author_email = 'd0n@janeiskla.de'
classifiers = ['Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: System Administrators',
               'Intended Audience :: Information Technology',
               'License :: OSI Approved :: ' \
                   'GNU General Public License v3 or later (GPLv3+)',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Security',
               'Topic :: Security :: Cryptography',
               'Topic :: Desktop Environment',
               'Topic :: Utilities',
               'Topic :: Desktop Environment']

include_package_data = True
long_description = 'utility to manage pavlov\'s rcon like admin interface'

entry_points = {
    'console_scripts': ['pavlovadm = pavlovadm.__init__:pavlovadm']}

package_data = {
    '': ['pavlovadm/example']}

data_files=[
    ('share/pavlovadm', [
        'pavlovadm/example/BalancingTable.csv', 'pavlovadm/example/Game.ini', 'pavlovadm/example/public.ini'])]

