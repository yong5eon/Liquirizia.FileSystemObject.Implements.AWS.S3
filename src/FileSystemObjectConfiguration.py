# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject.FileSystemObjectConfiguration import FileSystemObjectConfiguration as FileSystemObjectConfigurationBase

__all__ = (
	'FileSystemObjectConfiguration'
)


class FileSystemObjectConfiguration(FileSystemObjectConfigurationBase):
	"""
	File System Object Configuration Class for Amazon Web Service S3
	"""
	def __init__(self, bucket, token, secret, region, version=None):
		self.bucket = bucket
		self.accessKey = token
		self.accessSecretKey = secret
		self.region = region
		self.version = version
		return
