from setuptools import setup, find_packages

with open("README.md","r") as ofile:
    long_description_file = ofile.read()
    
setup(
    name='signapse',
    version='1.0.19',
    description='Signapse_synthetic_signer',
    long_description=long_description_file,
    long_description_content_type="text/markdown",
    author='Basheer Alwaely',
    author_email='basheer@signapse.ai',
    url='https://github.com/signapse/signapse',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>3.7',
)
