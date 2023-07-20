# Liquirizia.FileSystemObject.Implements.AWS.S3
FileSystemObject Implementation of Liquirizia for AWS S3

## Sample
```python
from Liquirizia.FileSystemObject import FileSystemObjectHelper
from Liquirizia.FileSystemObject.Implements.AWS.S3 import FileSystemObject, FileSystemObjectConfiguration

if __name__ == '__main__':
	# set file system to use
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

	# load file system object with name
	fso = FileSystemObjectHelper.Get('Sample')
	
	# create file in file system
	fso.create('YOUR_PATH', format='text/plain', charset='utf-8', filename='Sample.txt')

	# write file 
	with fso.open(path) as f:
		f.write('YOUR_DATA'.encode('utf-8'))
		f.close()

	# read file
	with fso.open(path) as f:
		print(f.read())
		f.close()
```

## Depends
* Liquirizia - https://github.com/team-of-mine-labs/Liquirizia
* boto3
