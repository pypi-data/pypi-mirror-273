"""cookiecutter distutils configuration."""
from pathlib import Path
from setuptools import setup, find_packages
from scnx_soar_integration_sdk.__init__ import __version__


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
    'arrow',
    'rich',
    'cookiecutter',
    'jsonmerge',
    'astunparse'
]


setup(
    name='scnx_soar_integration_starter',
    version=__version__,
    description=(
        'A command-line utility that creates Python package project template.'
        'This newly created project will have boiler plate code for integrations.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ashish Gupta',
    author_email='ashishkrgupta@hotmail.com',
    url='https://bitbucket.org/securonixsnypr/scnx-soar-integration-sdk/src/develop/',
    project_urls={
        "Documentation": "https://securonix.atlassian.net/wiki/spaces/S6R/pages/3587407928/Integration+Project+Generator+CLI+Design",
        "Issues": "https://securonix.atlassian.net/browse/SOAR-9659"
    },
    packages=find_packages(exclude=[]),
    package_dir={'scnx-soar-integration-starter': 'scnx-soar-integration-starter'},
    entry_points={'console_scripts': ['scnx_soar_integration_sdk = scnx_soar_integration_sdk.__main__:main', 'scnx_soar_integration_reload = scnx_soar_integration_sdk.__main__:reload']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=requirements,
    license='BSD',
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "scnx-soar-integration-sdk",
        "scnx-soar-integration-starter",
        "Python",
        "projects",
        "project templates",
        "project directory",
        "package",
        "packaging",
    ],
)