# -*- coding: utf-8 -*-

from Liquirizia.FileSystemObject import Helper
from Liquirizia.FileSystemObject.Implements.AWS.S3 import Connection, Configuration
from Liquirizia.System.Util import GenerateUUID

if __name__ == '__main__':
	Helper.Set(
		'Sample',
		Connection,
		Configuration(
			bucket='YOUR_BUCKET',
			token='YOUR_TOKEN',
			secret='YOUR_TOKEN_SECRET',
			region='YOUR_REGION',
			version='YOUR_VERSION',
		)
	)

	fso = Helper.Get('Sample')
	path = 'YOUR_PATH'.format(GenerateUUID())
	fso.create(path, format='text/plain', charset='utf-8', filename='Sample.txt')

	with fso.open(path) as f:
		f.write('hello world'.encode('utf-8'))
		f.close()

	with fso.open(path) as f:
		print(f.read())
		f.close()

