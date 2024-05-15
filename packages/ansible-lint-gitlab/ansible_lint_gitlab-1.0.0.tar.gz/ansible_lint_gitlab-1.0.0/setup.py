import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansible-lint-gitlab",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version="1.0.0",
    author="DevAlphaKilo",
    author_email="DevAlphaKilo@gmail.com",
    description="Converts ansible-lint JSON output into GitLab friendly format (JUnit XML, Codeclimate)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devalphakilo/ansible-lint-gitlab",
    keywords=['ansible', 'json', 'gitlab', 'ci/cd', 'xml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ['ansible-lint-gitlab = ansible_lint_gitlab.reporter:main']
    },
    install_requires=[
        'ansible-lint',
        'junit-reporter'
    ],
    setup_requires=[],
    python_requires=">=3.6",
)