from setuptools import setup, find_packages

setup(
    name='basharmor',
    version='3.1.0',
    packages=find_packages(),
    install_requires=['requests', 'pyinstaller'],
    entry_points={
        'console_scripts': [
            'basharmor=basharmor.module:main',
        ],
    },
    author='Aji Permana',
    author_email='admin@cybervpn.site',
    description='A Python module for installing and configuring Basharmor',
    long_description='Basharmor is a free file compiler and encryption obfuscate with up-to-date encryption.',
    url='https://github.com/Azigaming404',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    data_files=[('/usr/bin', ['basharmor/.load'])],  # Masukkan file tambahan di sini
    options={
        'install': {
            'mode': '755',  
        },
    },
)

