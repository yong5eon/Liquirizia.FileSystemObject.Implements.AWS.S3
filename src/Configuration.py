# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject import Configuration as BaseConfiguration

__all__ = (
	'Configuration'
)


class Configuration(BaseConfiguration):
	"""File System Object Configuration Class for Amazon Web Service S3"""

	def __init__(self, bucket, token, secret, region, version=None):
		self.bucket = bucket
		self.accessKey = token
		self.accessSecretKey = secret
		self.region = region
		self.version = version
		return
