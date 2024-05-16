from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A base to create new packages'
LONG_DESCRIPTION = 'A base to create new packages'

setup(
    name="base_package_velsis",
    version=VERSION,
    author="Maykon Schier",
    author_email="maykonschier@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests', 'py-zabbix'],
    keywords=['python', 'base'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
    ]
)