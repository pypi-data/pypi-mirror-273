from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
here_qualys_tbx = pathlib.Path(here, "qualys_tbx")

# Get the long description from the README file
long_description = (here_qualys_tbx / 'README.md').read_text(encoding='utf-8')


setup(
    name='qualystbx',
    version='0.1.0',
    packages=find_packages(include=[
        'qualys_tbx',
        'qualys_tbx.qtbx_lib',
        'qualys_tbx.qtbx_policy_merge',
        'qualys_tbx.*',
        'qualys_tbx.qtbx_lib.*',
        'qualys_tbx.qtbx_policy_merge.*',
    ]),
    #scripts=['bin/*.*'],
    url='https://pypi.org/project/qualystbx/',
    project_urls={
        'Documentation': 'https://dg-cafe.github.io/qualystbx/',
    },
    keywords='qualys, qualystoolbox, qualys.com, david gregory, qualystbx, qualysapi',

    license='Apache',
    author='David Gregory',
    author_email='dgregory@qualys.com, dave@davidgregory.com',
    description='Qualys Tool Box - Tools for running various functions in Qualys.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.9.0',
    package_data={'': ['*.yaml', '.*.yaml', '*.sh', '*.md']},
)
