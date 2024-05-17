from setuptools import find_packages, setup

with open('README.md','r') as f:
    long_description = f.read()
    
setup(
    name="ai-server-sdk",                     # This is the name of the package
    version="0.0.16",
    packages=find_packages(),
    install_requires=[
        'requests', 
        'pandas', 
        'jsonpickle'
    ], 
    author="Thomas Trankle, Maher Khalil",                     # Full name of the author
    description="Utility package to connect to AI Server instances.",
    license="MIT",
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)