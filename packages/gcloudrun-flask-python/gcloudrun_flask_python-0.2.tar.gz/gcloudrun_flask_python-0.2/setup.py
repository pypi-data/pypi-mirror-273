from setuptools import setup, find_packages

setup(
    name='gcloudrun_flask_python',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.3',
        'gunicorn==22.0.0',
        'Werkzeug==3.0.3'
    ],
    entry_points={
        'console_scripts': [
            'gcloudrun_flask_python = gcloudrun_flask_python.cli:main'
        ]
    }
)
