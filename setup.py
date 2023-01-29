from setuptools import find_packages, setup

long_description = (
    open("README.md", "rb").read().decode("utf-8")
)

setup(
    name="mosparo",
    version="1.0.0",
    description="Python API Client to communicate with mosparo.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="mosparo Core Developers",
    author_email="info@mosparo.io",
    keywords=['mosparo', 'spam-protection', 'accessibility', 'captcha'],
    license="MIT",
    url="https://github.com/mosparo/python-api-client",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
    ],
    packages=find_packages(),
    install_requires=['requests'],
    setup_requires=['pytest-runner', 'requests-mock'],
    tests_require=['pytest'],
    test_suite='tests',
    include_package_data=True,
    python_requires='>=3.5',
)