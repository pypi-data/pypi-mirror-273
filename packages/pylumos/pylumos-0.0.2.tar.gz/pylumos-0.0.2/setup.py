
from setuptools import setup, find_packages

setup(
    name='pylumos',
    version="0.0.2",
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    license='MIT',
    author='Adrian Rothenbuhler',
    author_email='adrian@redhill-embedded.com',
    description='Addressable LED interface tool',
    keywords='LED',
    url='https://github.com/redhill-embedded/recom.git',
    #download_url='https://github.com/redhill-embedded/lumos/archive/v_010.tar.gz',
    package_data={
        "lumos": [
            "package_version"
        ]
    },
    python_requires=">=3.8",
    install_requires=["recom==0.0.3"],
    entry_points={
        "console_scripts": [
            "lumos=lumos.__main__:main",
        ]
    },
)