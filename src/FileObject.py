# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject.FileObject import FileObject as FileObjectBase
from Liquirizia.FileSystemObject.Error import *

from botocore.exceptions import ClientError

__all__ = (
	'FileObject'
)


class FileObject(FileObjectBase):
	"""
	File Object Class for Amazon Web Service S3
	"""
	def __init__(self, fso):
		self.fso = fso
		self.fo = None
		self.stream = None
		return

	def __del__(self):
		if self.fo:
			self.close()
		return

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		return

	def open(self, path, mode='r'):
		try:
			self.fo = self.fso.bucket.Object(path)
			if 'r' in mode:
				response = self.fo.get()
				self.stream = response['Body']
		except Exception as e:
			raise FileNotFoundError(path, error=e)
		return

	def read(self, size=None):
		try:
			if not self.stream:
				raise RuntimeError('File is not readable')
			if size:
				return self.stream.read(size)
			buffer = bytes()
			while True:
				buf = self.stream.read()
				if not buf:
					break
				buffer += buf
			return buffer
		except ClientError as e:
			raise ConnectionClosedError('Can\'t read file({})'.format(str(e)), error=e)

	def readline(self):
		if not self.stream:
			raise RuntimeError('File is not readable')
		return self.stream._raw_stream.readline()

	def write(self, buffer):
		try:
			params = {}
			try:
				if self.fo.content_type:
					params['ContentType'] = self.fo.content_type
			except ClientError:
				pass
			try:
				if self.fo.content_encoding:
					params['ContentEncoding'] = self.fo.content_encoding
			except ClientError:
				pass
			try:
				if self.fo.content_disposition:
					params['ContentDisposition'] = self.fo.content_disposition
			except ClientError:
				pass
			try:
				if self.fo.content_language:
					params['ContentLanguage'] = self.fo.content_language
			except ClientError:
				pass
			self.fo.put(Body=buffer, **params)
		except ClientError as e:
			raise ConnectionClosedError('Can\'t write file({})'.format(str(e)), error=e)
		return

	def close(self):
		if self.fo:
			self.fo = None
		return
