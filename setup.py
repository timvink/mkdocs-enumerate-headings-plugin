from setuptools import setup, find_packages

setup(
    name='mkdocs-index-plugin',
    version='1.0.0',
    description='A MkDocs plugin to add index to titles of every page.',
    long_description='A MkDocs plugin to add index to titles of every page.\n'
                     '[options]:\n'
                     'strict_mode: True\n'
                     '     In this mode, you must edit head from h1 level by level, '
                     'such as "# first\\n## second\\n# first2".'
                     'Not allowed to over level, such as "# first\\n### third\\n# first2".\n'
                     '     Otherwise, if you do not deternmine the option or False.'
                     'You could edit head level in ascending order.The example above is allowed, it will be convert to'
                     ' "# 1 first\\n### 1.1 third\\n# 2 first2".\n',
    keywords='mkdocs index plugin',
    url='',
    author='shihr',
    author_email='shrshraa@outlook.com',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-index-plugin=mkdocs_index_plugin.plugin:AddIndexPlugin'
        ]
    }
)
