from setuptools import setup, find_packages

setup(
    name='selenium_utils_xmlangel',
    version='0.0.3',
    description='PYPI selenium-utils package creation written by xmlangel',
    author='xmlangel',
    author_email='kwangmyung.kim@gmail.com',
    url='https://github.com/xmlangel/selenium-utils-xmlangel',
    install_requires=['opencv-python', 'scikit-image', ],
    packages=find_packages(exclude=[]),
    keywords=['selenium', 'xmlangel', 'utils'],
    python_requires='>=3.12',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
