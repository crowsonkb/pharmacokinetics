from setuptools import setup

setup(
    name='pharmacokinetics',
    version='0.1.0',
    description='A Flask web application to calculate and plot drug concentration over time.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/crowsonkb/pharmacokinetics',
    author='Katherine Crowson',
    author_email='crowsonkb@gmail.com',
    license='MIT',
    packages=['pk', 'pk_webapp'],
    data_files=[('', ['.flaskenv', 'demo.svg', 'LICENSE', 'README.md', 'uwsgi.ini'])],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=1.0.2',
        'matplotlib>=2.2.2',
        'numpy>=1.14.3',
        'pyparsing>=2.3.0',
        'python-dotenv>=0.10.0',
        'scipy>=1.1.0',
    ],
    entry_points={
        'console_scripts': ['pk=pk.cli:main'],
    },
)
