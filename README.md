QINIUFS
=======

[![Version](https://img.shields.io/pypi/v/qiniufs.svg)](https://pypi.python.org/pypi/qiniufs)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/blindspoter/qiniufs/master/LICENSE)

Qiniu file uploader for Flask


## Install

```
$ pip install qiniufs
```

## Usage

```python
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
```

