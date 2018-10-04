from botocore.exceptions import ClientError
from mimetypes import guess_type
from pathlib import Path

"""Class for Managing S3."""
class BucketMgr:
    """BucketMgr."""

    def __init__(self, session):
        """Create a BucketMgr Object."""
        self.session = session
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Get all buckets iterator."""
        return self.s3.buckets.all()

    def all_objs(self, bucket_name):
        """Get an iterator all bucket objects."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create new bucket, or return exisitng bucket."""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':                
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    def set_policy(self, bucket):
        """Set bucket policy (read everyone)."""
        policy = """
        {
            "Version":"2012-10-17",
            "Statement":[
                {
                    "Sid":"PublicReadGetObject",
                    "Effect":"Allow",
                    "Principal":"*",
                    "Action":["s3:GetObject"],
                    "Resource":["arn:aws:s3:::%s/*"]
                }
            ]
        }
        """ % bucket.name
        policy = policy.strip()
        policy_obj = bucket.Policy()
        policy_obj.put(Policy=policy)

    def config_website(self, bucket, index, error):
        """Configure static site."""
        ws = bucket.Website()
        ws.put(WebsiteConfiguration={'ErrorDocument': {'Key': error}, 'IndexDocument': {'Suffix': index}})
        url = "http://%s.s3-website.%s.amazonaws.com" % (bucket.name, self.session.region_name)
        return url

    def upload_file(self, bucket, path, key):
        """Upload a file to bucket."""
        content_type = guess_type(key)[0] or 'application/octet-stream'
        return bucket.upload_file(path, key, ExtraArgs = {'ContentType': content_type })

    def sync(self, pathname, bucket_name):
        """ sync directory to bucket."""
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()

        def handle_dir(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_dir(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))
        handle_dir(root)