from setuptools import setup


setup(
        name='weather',
        version='0.0.1',
        py_modules=['cli'],
        install_requires=[
            'requests',
            'click',
        ],
        #entry_points='''
        #    [console_scripts]
        #    cli=cli:main
        #''',
        entry_points = {
                'console_scripts':
                    ['weather=cli:main'],
            }
    )
