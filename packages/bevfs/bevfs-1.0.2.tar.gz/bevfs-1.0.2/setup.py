from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bevfs',
    version='1.0.2',
    author='Mohammed Bilal Shakeel',
    author_email='mohammedbilalshakeel@gmail.com',
    description='A package for feature selection in high dimensional data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Bilal39/Bird-Eye-View/tree/main',
    packages=find_packages(),  # Automatically discover and include all packages
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Define minimum Python version required
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'scikit-learn>=0.24.0',
    ],
)
