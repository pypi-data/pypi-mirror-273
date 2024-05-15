from setuptools import setup, find_packages



with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='KudraCloudClient',
    version='0.0.15',
    author='UBUAI Inc',
    author_email='admin@ubiai.tools',
    description='A client for Kudra Cloud',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ubiai-incorporated/KudraCloudClient",
    project_urls = {
        "Bug Tracker": "https://github.com/ubiai-incorporated/KudraCloudClient",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    python_requires = ">=3.8",
    requires=[
        "tuspy",
        "requests"
    ]
)