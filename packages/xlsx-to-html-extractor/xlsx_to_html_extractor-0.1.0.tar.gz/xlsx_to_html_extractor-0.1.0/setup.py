from setuptools import setup, find_packages

setup(
    name='xlsx-to-html-extractor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'pandas',
    ],
    include_package_data=True,
    description='A Python utility to convert Excel sheets to HTML files, with options to include formulas, grid labels, and cell titles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/markolofsen/xlsx-to-html-extractor',
    author='Mark',
    author_email='markolofsen@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
