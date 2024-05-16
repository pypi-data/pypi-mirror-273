from setuptools import setup, find_packages


setup(
    name='shared_storage_client_5',
    version='0.1.0',
    author='Chris Maresca',
    author_email='chris@workmait.ai',
    description='Storage Client For Microservices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),  # Look for packages in the 'src' directory
    package_dir={'': 'src'},  # Specify the root package directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'boto3',
        's3fs',
        'python-dotenv',
    ],
)
