import setuptools

PACKAGE_NAME = 'contact-person-profile-csv-imp-local'
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.8',  # https://pypi.org/project/contact-person-profile-csv-imp-local/
    author="Circles",
    author_email="info@circles.ai",
    description="PyPI Package for Circles CSVToContactPersonProfile-local Local/Remote Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'contact-local>=0.0.42',
        'logger-local>=0.0.135',
        'database-mysql-local>=0.0.290',
        'user-context-remote>=0.0.77'
    ]
)
