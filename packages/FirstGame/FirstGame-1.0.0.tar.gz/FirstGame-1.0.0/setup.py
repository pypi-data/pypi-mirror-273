from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FirstGame',
    version='1.0.0',
    author="spx220",
    author_email="eric2173459@gmail.com",
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    packages=['FirstGame'],
    license='MIT',
    zip_safe=False,
    keywords=['spx', 'kpop', 'anime', 'FirstGame'],
    install_requires=[
        'pygame==2.5.2',
        'pymysql==1.1.0',
        'pillow==10.2.0',
        'pyyaml==6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'my_project=main:main',
        ],
    },
)