from setuptools import find_packages, setup

long_description = (
    open("README.md", "rb").read().decode("utf-8")
)

setup(
    name="mosparo",
    version="1.0.0",
    description="Python API Client to communicate with mosparo.",
    long_description=long_description,
    author="mosparo Core Developers",
    author_email="info@mosparo.io",
    keywords=['mosparo', 'spam-protection', 'accessibility', 'captcha'],
    license="MIT",
    url="https://github.com/mosparo/python-api-client.git",
    packages=find_packages(include=['mosparo']),
    install_requires=['requests'],
    setup_requires=['pytest-runner', 'requests-mock'],
    tests_require=['pytest'],
    test_suite='tests'
)