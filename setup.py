from setuptools import setup, find_packages

setup(name='MacSAFER',
    version='1.1',
    url='https://github.com/thy2134/MacSAFER',
    license='GPLv3',
    author='Kyujin Cho',
    author_email='thy2134@gmail.com',
    description='Delete malicious plugins from korean e-commerce, government, online banking websites to make your mac clean.',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Environment :: MacOS X',
        'Environment :: Console'
    ],
    packages=find_packages(exclude=['test', 'doc']),
    zip_safe=False,
    entry_points= {
        'console_scripts': ['macsafer=macsafer.command_line:main']
    }
)