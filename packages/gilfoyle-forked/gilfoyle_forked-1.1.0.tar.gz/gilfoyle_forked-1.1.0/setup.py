from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gilfoyle-forked',
    packages=['gilfoyle'],
    version='1.1.0',
    license='MIT',
    description='Gilfoyle is a Python-based report generator for data scientists who use Pandas.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shahab Rashid',
    author_email='sr.python10@gmail.com',
    url='https://github.com/sr-auto/gilfoyle',
    download_url='https://github.com/sr-auto/gilfoyle/archive/master.zip',
    keywords=['python', 'reports', 'reporting', 'pandas', 'pdf'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['pandas', 'weasyprint', 'jinja2', 'seaborn'],
    include_package_data=True
)
