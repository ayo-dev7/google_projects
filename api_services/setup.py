from setuptools import setup, find_packages

setup(
    name='api-services',  
    version='0.1.0',          
    author='Damilola Adebiyi',  
    author_email='ayoadebiyi95@gmail.com',  
    description='A package for Google API services', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/ayo-dev7/google_projects',  
    packages=find_packages(where='api_services'),  # Automatically find and include packages
    package_dir={'':'api_services'},
    install_requires=[
        'cachetools==5.5.0',
        'google-api-python-client==2.146.0',
        'google-auth==2.35.0',
        'google-auth-oauthlib==1.2.1',
        'httplib2==0.22.0',
        'pandas==2.2.3',
        'requests==2.32.3',
        'requests-oauthlib==2.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust as necessary
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify minimum Python version
)