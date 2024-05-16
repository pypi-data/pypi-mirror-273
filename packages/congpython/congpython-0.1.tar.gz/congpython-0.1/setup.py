from setuptools import setup, find_packages

setup(
    name='congpython',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    author='Cong Le',
    author_email='cong.lt91@gmail.com',
    description='các function cho cong',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)