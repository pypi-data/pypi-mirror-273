from setuptools import setup, find_packages

setup(
    name='newguy103-syncserver',
    version='1.2.0',
    author='NewGuy103',
    author_email='userchouenthusiast@gmail.com',
    description='newguy103-syncserver simplifies file synchronization using Flask-based server and client modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'syncserver-server = syncserver.server.__main__:main',
            'syncserver-server.db = syncserver.server._db:run_cli'
        ]
    },
    install_requires=[
        'cryptography',
        'newguy103-pycrypter',
        'requests',
        'flask',
        'argon2-cffi',
        'msgpack'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
    include_package_data=True,
    package_data={
        '': ['README.md'],
        'syncserver': ['client/*.py', 'server/*.py'],
    },
)
