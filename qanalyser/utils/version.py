#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_version():
    """Return a PEP 440-compliant version number from VERSION"""

    from qanalyser import VERSION as version

    main = '{major}.{minor}'.format(
        major=version.get('major'),
        minor=version.get('minor')
    )

    if version.get('micro') != 0:
        main += '.{micro}'.format(micro=version.get('micro'))

    sub = ''
    if version.get('release') != 'final':
        mapping = {
            'alpha': 'a',
            'beta': 'b',
            'release-candidate': 'rc'
        }
        sub += mapping[version.get('release')] + str(version.get('relnum'))
    if version.get('post'):
        sub += '.post{}'.format(version.get('postnum'))
    if version.get('dev'):
        sub += '.dev{}'.format(version.get('devnum'))

    return main + sub
