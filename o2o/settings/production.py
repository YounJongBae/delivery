
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']

# AWS settings
AWS_ACCESS_KEY_ID = "AKIAJRAG2MYLWOB3M34A"
AWS_SECRET_ACCESS_KEY = "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"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True
AWS_S3_HOST = "s3-ap-northeast-2.amazonaws.com"
DEFAULT_FILE_STORAGE = 'o2o.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'awsbean-bucket-project'
S3DIRECT_REGION = 'ap-northeast-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
import datetime
date_two_months_later = datetime.date.today() + datetime.timedelta(2 * 365 / 12)
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=86400',
}
AWS_DEFAULT_ACL = None
