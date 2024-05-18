import setuptools

PACKAGE_NAME = "person-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.60',  # https://pypi.org/project/person-local/
    author="Circles",
    author_email="info@circles.ai",
    description="PyPI Package for Circles person Local Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "database-infrastructure-local>=0.0.24",
        "database-mysql-local>=0.0.290",
        "email-address-local>=0.0.40",
        "language-remote>=0.0.20",
        "logger-local>=0.0.135",
        "user-context-remote>=0.0.75",
        "people-local>=0.0.13"
    ]
)
