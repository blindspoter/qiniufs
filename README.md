QINIUFS
=======

Qiniu file uploader for Flask


## Install
```
$ pip install qiniufs
```

## Usage
```python
bucket = "your-qiniu-bucket-name"
prefix_urls = "your-qiniu-url"
fs = QiniuFS(bucket, access_key, secret_key, prefix_urls)

def upload_picture(picture):
    mime = picture.mimetype
    data = picture.read()
    if data:
        r, d = fs.upload(data, mime)
    if r and d:
        key = d.get('key')
        url = fs.get_url(d.get('key'))
        return key, url
```
