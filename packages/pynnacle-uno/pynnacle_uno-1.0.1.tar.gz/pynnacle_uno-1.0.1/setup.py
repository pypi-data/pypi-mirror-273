from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='pynnacle_uno',
    version='1.0.1', 
    packages=find_packages(),
    description='A Python module that provides hands-on robotics coding experience in Python that closely mirrors the structure and functionality of Arduino\'s programming language.',
    url='https://github.com/Red-Pula/Pynnacle-Uno',
    author='Rafael Red Angelo M. Hizon, Jenel M. Justo, Serena Mae C.S. Lee',
    author_email='redhizon@gmail.com, jenel.just88@gmail.com, nmae.lee@gmail.com',
    license='GNU Affero General Public License',
    install_requires=['pymata4>=1.15'],
    long_description=description,
    long_description_content_type="text/markdown",

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
