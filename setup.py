from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-add-number-plugin',
    version='1.1.0',
    description='MkDocs Plugin to automatically number the headings (h1-h6) in each markdown page.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs index add-number plugin',
    url='https://github.com/shihr/mkdocs-add-number-plugin.git',
    author='shihr',
    author_email='shrshraa@outlook.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-add-number-plugin=mkdocs_add_number_plugin.plugin:AddNumberPlugin',
            'add-number=mkdocs_add_number_plugin.plugin:AddNumberPlugin' 
        ]
    }
)
