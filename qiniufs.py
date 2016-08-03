# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import urlparse
import qiniu

from .randbytes import randbytes2


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
    def __init__(self, bucket, access_key, secret_key, prefix_url, policy=None):
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key
        self.prefix_url = prefix_url
        self.policy = policy

    def __repr__(self):
        return '<QiniuFS %s>' % self.bucket

    def _make_auth(self):
        return qiniu.Auth(self.access_key.encode('ascii'),
                          self.secret_key.encode('ascii'))

    def _token(self, key=None, expires=3600):
        """
        token
        """
        key = key or randbytes2(16)
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


class QiniuPolicy(object):
    '''
    http://developer.qiniu.com/article/developer/security/put-policy.html
    '''
    def __init__(self,
                 bucket,
                 callback_url=None,
                 callback_body=None,
                 return_url=None,
                 return_body=None,
                 persistent_ops=None,
                 persistent_notify_url=None,
                 persistent_pipeline=None,
                 delete_after_days=None):

        self.policy = {}
        self.bucket = bucket

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
