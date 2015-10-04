try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from koi import __version__

setup(
    name='koi',
    version=__version__,
    description='3rd-party Aliyun python client which supports python3',
    url='https://github.com/observerss/koi',
    author='Jingchao Hu(observerss)',
    author_email='jingchaohu@gmail.com',
    packages=['koi'],
    package_data={'': ['LICENSE']},
    license=open('LICENSE').read(),
    install_requires=[
        'requests>=2.7',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
