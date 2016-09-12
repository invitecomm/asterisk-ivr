"""Packaging files and information."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from ivr import __version__ as version

setup(
    name = 'ivr',
    packages = ['ivr'], # this must be the same as the name above
    version = version,
    description = 'AGI Controlled IVR for Asterisk',
    author = 'Brian LaVallee',
    author_email = 'brian.lavallee@invite-comm.jp',
    url = 'https://github.com/invitecomm/asterisk-ivr', # use the URL to the github repo
    download_url = 'https://github.com/invitecomm/asterisk-ivr/tarball/' + version, # I'll explain this in a second
    keywords = 'python asterisk agi ivr telephony telephony sip voip',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
    ],
    license = 'GNU GENERAL PUBLIC LICENSE',

    # Package dependencies:
    install_requires = ['six>=1.9.0','google-api-python-client==1.5.3','pyst2'],
    
)