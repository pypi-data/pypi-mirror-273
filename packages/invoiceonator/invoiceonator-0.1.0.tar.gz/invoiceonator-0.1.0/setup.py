from setuptools import setup, find_packages

setup(
    name='invoiceonator',
    version='0.1.0',
    description='A tool to generate invoice templates and PDFs from YAML files',
    author='Charles Watkins',
    author_email='chris@watkinslabs.com',
    url='https://github.com/yourusername/invoiceonator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Pillow',
        'reportlab',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'invoiceonator=invoiceonator.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
)
