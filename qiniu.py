# -*- coding: utf-8 -*-

from __future__ import absolute_import

import qiniu
from .randbytes import randbytes2
import app.config as config


class QiniuFS(object):
    '''
    七牛云存储
    Attributes:
        bucket_name: 存储空间
        prefix_urls: 存储空间URL前缀
        policy:      存储空间上传策略
    '''
    def __init__(self, bucket_name, prefix_urls, policy=None):
        self.bucket_name = bucket_name
        self.prefix_urls = prefix_urls
        self.policy = policy

    def __repr__(self):
        return '<QiniuFS %s>' % self.bucket_name

    def _make_auth(self):
        return qiniu.Auth(config.QINIU_AK.encode('ascii'),
                          config.QINIU_SK.encode('ascii'))

    def _token(self, key=None, expires=3600):
        """
        生成上传凭证
        """
        key = key or randbytes2(16)
        auth = self._make_auth()
        token = auth.upload_token(self.bucket_name, key=key, expires=expires, policy=self.policy)
        return token, key

    def upload_data(self, data, mime_type=None, key=None):
        """
        直接上传二进制流
        Args:
            data:      二进制流对象
            key:       文件名
            mime_type: 上传数据的mimeType

        Returns:
            True or False 和 {"hash": "<Hash string>", "key": "<Key string>"}
        """
        token, key = self._token(key)
        mime_type = mime_type or 'application/octet-stream'
        ret, info = qiniu.put_data(token, key, data, mime_type=mime_type)
        if ret is None:
            raise UploadError(ret, info)
        return (True, ret)

    def upload_file(self, file, mime_type=None, key=None):
        """
        断点续传上传文件
        Args:
            file:      文件对象
            key:       文件名
            mime_type: 上传数据的mimeType

        Returns:
            True or False 和 {"hash": "<Hash string>", "key": "<Key string>"}
        """
        token, key = self._token(key)
        mime_type = mime_type or 'application/octet-stream'
        data_size = len(file.read())
        ret, info = qiniu.put_stream(token, key, file, data_size, mime_type=mime_type,
                                     progress_handler=lambda progress, total: progress)
        if ret is None:
            raise UploadError(ret, info)
        return (True, ret)


class UploadError(Exception):
    pass
