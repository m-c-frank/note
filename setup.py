from setuptools import setup, find_packages

setup(
    name='note',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'note=note.main:cli',
        ],
    },
    install_requires=[
        "fire"
    ],
    python_requires='>=3.9',
)
