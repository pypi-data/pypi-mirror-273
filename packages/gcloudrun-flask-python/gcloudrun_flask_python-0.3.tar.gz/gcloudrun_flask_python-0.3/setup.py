from setuptools import setup, find_packages

setup(
    name='gcloudrun_flask_python',
    version='0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gcloudrun_flask_python = gcloudrun_flask_python.cli:main'
        ]
    }
)
