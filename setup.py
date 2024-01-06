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
        'fire',
    ],
    author='Martin Christoph Frank',
    author_email='martinchristophfrank@gmail.com',
    description='take notes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://localhost:8080/mcfrank/note'
)

