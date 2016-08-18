# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import datetime
import urlparse
import qiniu
import binascii

POLICY_FILED = [
    'callbackUrl',
    'callbackBody',
    'returnUrl',
    'returnBody',
    'persistentOps',
    'persistentNotifyUrl',
    'persistentPipeline',
    'deleteAfterDays',
]


class QiniuFS(object):
    '''
    Qiniu file storage

    Attributes:
        bucket:      bucket name
        access_key:  access_key
        secret_key:  secret_key
        prefix_url:  domain
        policy:      policy for upload
    '''
    def __init__(self, bucket, access_key, secret_key, prefix_url, **kwargs):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.prefix_url = prefix_url
        self.policy = self.get_policy(**kwargs)

    def __repr__(self):
        return '<QiniuFS %s>' % self.bucket

    def _make_auth(self):
        return qiniu.Auth(self.access_key.encode('ascii'),
                          self.secret_key.encode('ascii'))

    def _token(self, key=None, expires=3600):
        """
        token
        """
        key = key or binascii.hexlify(os.urandom(16))
        auth = self._make_auth()
        token = auth.upload_token(self.bucket, key=key, expires=expires, policy=self.policy)
        return token, key

    def upload_data(self, data, mime_type=None, key=None):
        """
        upload data stream
        Args:
            data:      data stream
            key:       data stream name
            mime_type: data stream mimeType

        Returns:
            True or False and {"hash": "<Hash string>", "key": "<Key string>"}
        """
        token, key = self._token(key=key)
        mime_type = mime_type or 'application/octet-stream'
        ret, info = qiniu.put_data(token, key, data, mime_type=mime_type)
        if ret is None:
            raise UploadError(ret, info)
        return (True, ret)

    def upload_file(self, file, mime_type=None, key=None):
        """
        upload file object
        Args:
            file:      file object
            key:       file name
            mime_type: file mimeType

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
        delete the file form qiniu
        """
        auth = self._make_auth()
        bucket = qiniu.BucketManager(auth)
        ret, info = bucket.delete(self.bucket, key)
        return True, ret

    def asyn_file_process(self, key, fops, pipeline=None):
        """
        asynchronous file persistence
        """
        auth = self._make_auth()
        pfop = qiniu.PersistentFop(auth, self.bucket, pipeline=pipeline)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(key, ops, force=True)
        return True, ret

    def get_url(self, key, scheme='http', style=None, is_private=False):
        """
        url for the uploaded file
        """
        url = ''
        if self.prefix_url:
            url = urlparse.urljoin(self.prefix_url, '/' + key.rstrip('/'))
        else:
            url = ('http://%s.qiniudn.com/' % self.bucket) + key

        if style:
            url = url + '-' + style

        if is_private:
            expires = datetime.timedelta(hours=1)
            expires = int(expires.total_seconds())
            auth = self._make_auth()
            url = auth.private_download_url(url, expires=expires)
        return url

    def get_policy(self, **kwargs):
        '''
        http://developer.qiniu.com/article/developer/security/put-policy.html
        '''
        for key in kwargs:
            if key not in POLICY_FILED:
                raise UploadError("input the policy parameters error")
        return kwargs


class UploadError(Exception):
    pass
