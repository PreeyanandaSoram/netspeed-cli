from setuptools import setup, find_packages

setup(
    name='netspeed-cli',
    version='1.0.0',
    description='Internet speed test CLI tool',
    author='Preeyananda Soram',
    author_email='preeyananda@example.com',
    py_modules=['netspeed'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'netspeed=netspeed:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Initial',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
