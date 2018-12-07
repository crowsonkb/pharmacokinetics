from setuptools import setup

setup(
    name='pharmacokinetics',
    version='0.1.0',
    description='Calculates and plots drug concentration over time.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/crowsonkb/pharmacokinetics2',
    author='Katherine Crowson',
    author_email='crowsonkb@gmail.com',
    license='MIT',
    packages=['pk'],
    install_requires=[s.strip() for s in open('requirements.txt').readlines()],
    entry_points={
        'console_scripts': ['pk=pk.cli:main'],
    },
)
