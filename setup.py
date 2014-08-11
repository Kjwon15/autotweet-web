import os.path
import sys
from pip.req import parse_requirements

try:
    from setuptools import find_packages, setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


install_reqs = [str(ir.req) for ir in parse_requirements('requirements.txt')]
if sys.version_info < (3, 2):
    install_reqs.append('futures')


setup(
    name='autotweet-web',
    description='web instance for autotweet',
    long_description=readme(),
    url='http://kjwon15.net/',
    download_url='https://github.com/Kjwon15/autotweet-web/releases',
    author='Kjwon15',
    author_email='kjwonmail' '@' 'gmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=install_reqs,
)
