from setuptools import setup, find_packages

setup(
    name = 'iSwitch',
    version = '0.1.1',
    packages = find_packages(),
    install_requires = [
        'httpx',
        'simplejson',
        'colorlog'
    ],
    author = '#Einswilli',
    author_email = 'einswilligoeh@email.com',
    description = 'SwitchPay Python SDK for AllDotPy internal use. ',
    url = 'https://github.com/AllDotPy/iSwitch.git',
)