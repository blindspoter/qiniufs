"""
Install
```````
.. code::bash

pip install qiniufs

Usage
`````
.. code:: python

  # init
  bucket_name = "your-qiniu-bucket-name"
  prefix_url = "your-qiniu-domain"
  fs = QiniuFS(bucket_name, access_key, secret_key, prefix_url)

  # upload
  mime = data.mimetype
  r, d = fs.upload_data(data, mime=mime)
  if r and d:
      key = d.get('key')
      url = fs.get_url(d.get('key'))

  # delete
  r = fs.delete_file(key)
  if r:
      print "success"

Links
`````
* `github <https://github.com/blindspoter/qiniufs>`_

"""

from setuptools import setup

setup(
    name='qiniufs',
    version='1.0.2',
    url='https://github.com/blindspoter/qiniufs',
    license='MIT',
    author='kevinchen',
    author_email='wqchen.xjtuer@gmail.com',
    keywords='qiniu for flask',
    description='qiniu file uploader for flask!',
    long_description=__doc__,
    py_modules=['qiniufs'],
    platforms='any',
    install_requires=[
        'qiniu==7.1.7'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
