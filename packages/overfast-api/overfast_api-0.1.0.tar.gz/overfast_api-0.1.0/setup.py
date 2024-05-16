from setuptools import setup

setup(
    name='overfast_api',
    version='0.1.0',
    description='Wrapper for Overfast API',
    url='https://github.com/redjordan1202/OverfastAPI',
    author='Jordan Del Pilar',
    author_email='jordan@delpilar.net',
    license='MIT',
    packages=['overfast_api'],
    install_requires=[
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'urllib3',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
