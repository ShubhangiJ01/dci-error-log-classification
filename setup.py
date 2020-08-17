import codecs
import os
import setuptools

def _get_requirements():
    requirements_path = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)),
                                   'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = f.read()
        return requirements.split('\n')


def _get_readme():
    readme_path = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)),
                             'README.md')

    with codecs.open(readme_path, 'r', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='dci-error-log-classifier',
    version='0.0.1',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    author='Distributed ci team.',
    author_email='distributed-ci@redhat.com',
    description='Tool to label logs by the error type',
    long_description=_get_readme(),
    install_requires=_get_requirements(),
    license='Apache v2.0',
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Distributed Computing'
    ],
    entry_points={"console_scripts": ["dci-classifier = classifier.shell:main"]},
)