# setup.py

from setuptools import setup, find_packages

setup(
    name='jzai',
    version='59.83.39',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyttsx3',
        'SpeechRecognition',
        'nltk',
        'textblob',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jzai=jzai.cli:run',
        ],
    },
)
