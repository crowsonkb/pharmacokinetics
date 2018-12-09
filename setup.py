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
    install_requires=[s.strip() for s in open('requirements.txt').readlines()],
    entry_points={
        'console_scripts': ['pk=pk.cli:main'],
    },
    include_package_data=True,
    zip_safe=False,
)
