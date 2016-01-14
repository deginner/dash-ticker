from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3"
]

url = 'https://github.com/deginner/dashticker'

setup(
    name="dashticker",
    version="0.1.0",
    description='USD/DASH ticker service',
    author='Deginner',
    url=url,
    license='MIT',
    classifiers=classifiers,
    include_package_data=True,
    packages=['dashticker'],
    setup_requires=['pytest-runner'],
    install_requires=['websocket-client', 'redis', 'supervisor'],
    tests_require=['pytest', 'pytest-cov']
)
