# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject import Connection as BaseConnection
from Liquirizia.FileSystemObject.Errors import *

from .File import File
from .Configuration import Configuration

from boto3 import session
from botocore.client import Config
from botocore.exceptions import *

__all__ = (
	'FileSystemObject'
)


class Connection(BaseConnection):
	"""File Object Class for Amazon Web Service S3"""

	def __init__(self, conf: Configuration):
		self.conf = conf
		self.bucket = None
		self.client = None
		self.session = None
		return

	def __del__(self):
		self.close()
		return

	def connect(self):
		try:
			'''
			boto3 client와 resource가 내부적으론 하나의 글로벌 세션을 공유하기 때문에 thread safe 하지 않아
			로컬, 개발 등 하나의 인스턴스로 구성된 환경에서 동시다발적으로 connect 시도 시,
			간헐적으로 endpoint_resolver 에러가 나며 연결을 못하는 현상 발생.
			서비스 접근 정보가 동일하기 때문에 같은 세션으로 client와 resource의 연결을 묶어주어 임시 해결.
			참고: https://github.com/boto/boto3/issues/801
			'''
			self.session = session.Session()
			self.client = self.session.client(
				's3',
				aws_access_key_id=self.conf.accessKey,
				aws_secret_access_key=self.conf.accessSecretKey,
				region_name=self.conf.region,
				config=Config(signature_version='s3v4')
			)
			self.bucket = self.session.resource(
				's3',
				aws_access_key_id=self.conf.accessKey,
				aws_secret_access_key=self.conf.accessSecretKey,
				region_name=self.conf.region,
				config=Config(signature_version='s3v4')
			).Bucket(self.conf.bucket)
		except ClientError as e:
			raise ConnectionError('Can not connect bucket({}:{}:{}:{})'.format(self.conf.bucket, self.conf.accessKey, self.conf.accessSecretKey, self.conf.region), error=e)
		except Exception as e:
			raise ConnectionError('Can not connect bucket({}:{}:{}:{})'.format(self.conf.bucket, self.conf.accessKey, self.conf.accessSecretKey, self.conf.region), error=e)
		return

	def exist(self, path):
		try:
			metadata = self.client.head_object(
				Bucket=self.conf.bucket,
				Key=path
			)
			return True if metadata else False
		except ClientError as e:
			return False

	def stat(self, path):
		try:
			metadata = self.client.head_object(
				Bucket=self.conf.bucket,
				Key=path
			)
			# TODO : return FileStatObject
			return metadata
		except ClientError as e:
			raise ConnectionError('Can not connect bucket({}:{}:{}:{})'.format(self.conf.bucket, self.conf.accessKey, self.conf.accessSecretKey, self.conf.region), error=e)
		return

	def open(self, path, mode='r'):
		f = FileObject(self)
		f.open(path, mode)
		return f

	def close(self):
		if self.bucket:
			self.bucket = None
		if self.client:
			self.client = None
		return

	def create(self, path, format=None, charset=None, filename=None, locale=None):
		params = {}
		if format:
			params['ContentType'] = format
		if charset:
			params['ContentEncoding'] = charset
		if filename:
			params['ContentDisposition'] = 'filename={}'.format(filename)
		if locale:
			params['ContentLanguage'] = locale
		try:
			self.bucket.put_object(Key=path, **params)
		except ClientError as e:
			if e.response['Error']['Code'] == 'NoSuchBucket':
				raise Error('Bucket is not found({}:{}:{}:{})'.format(self.conf.bucket, self.conf.accessKey, self.conf.accessSecretKey, self.conf.region), error=e)
			raise Error(str(e), error=e)
		return

	def copy(self, src, dst):
		self.bucket.copy(src, dst)
		return

	def upload(self, path, expires=60*5):
		return self.client.generate_presigned_url(
			ClientMethod='put_object',
			Params={
				'Bucket': self.conf.bucket,
				'Key': path
			},
			ExpiresIn=expires
		)

	def download(self, path, expires=60*5):
		return self.client.generate_presigned_url(
			ClientMethod='get_object',
			Params={
				'Bucket': self.conf.bucket,
				'Key': path
			},
			ExpiresIn=expires
		)

	def files(self, path):
		li = []
		marker = None
		while True:
			response = self.client.list_objects(
				Bucket=self.conf.bucket,
				Prefix='{}/'.format(path),
				Delimiter='/',
				MaxKeys=1000,
				Marker=marker if marker else '',
			)
			for content in response['Contents']:
				li.append(content['Key'])
			if 'NextMarker' in response and response['NextMarker']:
				continue
			break
		return li if len(li) else None

