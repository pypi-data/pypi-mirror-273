from setuptools import setup, find_packages

setup(
    name='rid-ant',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'torch>=1.8.0',
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'altair>=4.0.0',
        'scipy>=1.4.0'
    ],
    author='Mbishu Fabrice',
    author_email='fmbishu@gmail.com',
    description='Python package for data analysis both quantitative and qualitative',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mbishu2002/rid',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
