from setuptools import setup, find_packages

setup(
    name='xursparks',
    version='1.0.9',
    packages=['xursparks'],
    python_requires=">=3.10",
    install_requires=[
        'requests',
        'pandas',
        'pyspark',
        'boto3',
        'ydata-profiling',
        'xurpas_data_quality',
    ],
    author='Randell Gabriel Santos',
    author_email='randellsantos@gmail.com',
    description='Encapsulating Apache Spark for Easy Usage',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dev-doods687/xursparks',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
