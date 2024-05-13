from setuptools import setup, find_packages

setup(
    name='adbmanager',
    version='0.0.3',
    packages=find_packages(),
    package_data={'adbmanager.modules': ['keyboard_events.json']},
    author='Frankelly Franco',
    author_email='francarium@gmail.com',
    description='simple adb manager for automate android',
    url='https://francarium.com/projects/adbmanager',
)
