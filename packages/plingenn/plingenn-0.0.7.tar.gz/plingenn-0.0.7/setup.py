from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='plingenn',
    version='0.0.7',
    description='A very basic package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Plingenn Plingsson',
    author_email='Plingenn12@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='none',
    packages=['plingenn'],
    install_requires=['requests', 'numpy']
)