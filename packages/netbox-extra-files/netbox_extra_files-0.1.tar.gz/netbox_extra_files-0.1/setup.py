from setuptools import find_packages, setup

setup(
    name='netbox-extra-files',
    version='0.1',
    description='Store extra files for objects in Netbox',
    url='https://github.com/emjemj/netbox-extra-files',
    author='Eric Lindsjö',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
