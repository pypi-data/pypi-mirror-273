from setuptools import setup

setup(
    name='linktest',
    version='2.7.9',
    author='Wang Lin',
    author_email='lin.wang.thinking@gmail.com',
    packages=['linktest'],
    install_requires=[
        "psutil",
        "requests",
        "pandas",
        "curlify",
        "selenium",
        "selenium-wire",
        "setuptools",
        "urllib3",
        "PyMySQL",
        "jsoncomparison",
        "chromedriver_autoinstaller"
    ],
)
