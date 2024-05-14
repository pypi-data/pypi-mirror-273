import setuptools

PACKAGE_NAME = "contact-phone-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.16',  # update only the minor version each time # https://pypi.org/project/contact-phone-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles contact-phone-local Python",
    long_description="PyPI Package for Circles contact-phone-local Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/contact-phone-local-python-package",  # https://pypi.org/project/contact-phone-local/
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.0',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'database-mysql-local>=0.0.290',
        'logger-local>=0.0.135',
        'phone-local>=0.0.15'
    ],
)
