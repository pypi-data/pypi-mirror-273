from setuptools import setup, find_packages

setup(
    name='mkdocs-roamlinks-with-pdf-plugin',
    version='2.0.0',
    description='An MkDocs plugin',
    long_description='An MkDocs plugin that automagically generates relative links and convert roamlike links for foam and obsidian between markdown pages',
    keywords='mkdocs',
    url= 'https://github.com/jokulab/mkdocs-roamlinks-plugin',
    author='jokulab',
    author_email='166611085+jokudev@users.noreply.github.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.0.4',
    ],
    extras_require={
        'dev': [ 'pytest']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'roamlinks-with-pdf = mkdocs_roamlinks_with_pdf_plugin.plugin:RoamLinksPlugin',
        ]
    }
)
