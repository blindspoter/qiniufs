"""
Install
```````

.. code:: bash

  pip install flask-qiniu

Links
`````

* `website <https://github.com/kevinchendev/flask-qiniu>`_

"""


from setuptools import setup

setup(
    name='flask-qiniu',
    version='0.0.1',
    url='https://github.com/kevinchendev/flask-qiniu',
    license='MIT',
    author='kevinchen',
    author_email='wqchen.xjtuer@gmail.com',
    keywords='GitHub flask-qiniu',
    description='qiniu file uploader for flask!',
    long_description=__doc__,
    py_modules=['qiniu'],
    platforms='any',
    install_requires=[
        'qiniu==7.0.6'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
