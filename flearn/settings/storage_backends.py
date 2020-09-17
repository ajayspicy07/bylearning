from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
	#default_acl = 'public'
	default_acl = 'public-read'
	location = 'media'
	file_overwrite = False
