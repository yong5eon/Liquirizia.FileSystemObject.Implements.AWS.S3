# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject import FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.AWS.S3 import FileSystemObject, FileSystemObjectConfiguration
from Liquirizia.System.Util import GenerateUUID

if __name__ == '__main__':
	FileSystemObjectHelper.Set(
		'Sample',
		FileSystemObject,
		FileSystemObjectConfiguration(
			bucket='YOUR_BUCKET',
			token='YOUR_TOKEN',
			secret='YOUR_TOKEN_SECRET',
			region='YOUR_REGION',
			version='YOUR_VERSION',
		)
	)

	fso = FileSystemObjectHelper.Get('Sample')
	path = 'YOUR_PATH'.format(GenerateUUID())
	fso.create(path, format='text/plain', charset='utf-8', filename='Sample.txt')

	with fso.open(path) as f:
		f.write('hello world'.encode('utf-8'))
		f.close()

	with fso.open(path) as f:
		print(f.read())
		f.close()

