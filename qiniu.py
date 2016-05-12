# -*- coding: utf-8 -*-

from __future__ import absolute_import

import qiniu
from .randbytes import randbytes2
import yourapp.config as config


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
        上传凭证
        """
        key = key or randbytes2(16)
        auth = self._make_auth()
        token = auth.upload_token(self.bucket_name, key=key, expires=expires, policy=self.policy)
        return token, key

    def upload_data(self, data, mime_type=None, key=None):
        """
        上传二进制流
        Args:
            data:      二进制流对象
            key:       文件名
            mime_type: 文件mimeType

        Returns:
            True or False 和 {"hash": "<Hash string>", "key": "<Key string>"}
        """
        token, key = self._token(key=key)
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
            mime_type: 文件mimeType

        Returns:
            True or False and {"hash": "<Hash string>", "key": "<Key string>"}
        """
        token, key = self._token(key=key)
        mime_type = mime_type or 'application/octet-stream'
        data_size = len(file.read())
        ret, info = qiniu.put_stream(token, key, file, data_size, mime_type=mime_type,
                                     progress_handler=lambda progress, total: progress)
        if ret is None:
            raise UploadError(ret, info)
        return (True, ret)

    def delete_file(self, key):
        """
        文件删除, 谨慎使用
        """
        auth = self._make_auth()
        bucket = qiniu.BucketManager(auth)
        ret, info = bucket.delete(self.bucket_name, key)
        return True, ret

    def asyn_file_process(self, key, fops, pipeline=None):
        """
        文件异步持久化处理
        """
        auth = self._make_auth()
        pfop = qiniu.PersistentFop(auth, self.bucket_name, pipeline=pipeline)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(key, ops, force=True)
        return True, ret


class QiniuPolicy(object):
    '''
    上传策略,字段含义请参考七牛文档
    http://developer.qiniu.com/article/developer/security/put-policy.html
    '''
    def __init__(self,
                 bucket_name,
                 callback_url=None,
                 callback_body=None,
                 return_url=None,
                 return_body=None,
                 persistent_ops=None,
                 persistent_notify_url=None,
                 persistent_pipeline=None,
                 delete_after_days=None):

        self.policy = {}
        self.bucket_name = bucket_name

        if callback_url:
            self.policy['callbackUrl'] = callback_url
        if callback_body:
            self.policy['callbackBody'] = callback_body
        if return_url:
            self.policy['returnUrl'] = return_url
        if return_body:
            self.policy['returnBody'] = return_body
        if persistent_ops:
            self.policy['persistentOps'] = persistent_ops
        if persistent_notify_url:
            self.policy['persistentNotifyUrl'] = persistent_notify_url
        if persistent_pipeline:
            self.policy['persistentPipeline'] = persistent_pipeline
        if delete_after_days:
            self.policy['deleteAfterDays'] = delete_after_days


class UploadError(Exception):
    pass
