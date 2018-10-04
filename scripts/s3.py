import boto3
from bucket import BucketMgr
import click

session = boto3.Session(profile_name='admin')
bucket_mgr = BucketMgr(session)

@click.group()
def cli():
    pass


@cli.command('list-buckets')
def listbuckets():
    """List buckets in AWS accounts."""
    for bucket in bucket_mgr.all_buckets():
        print(bucket)


@cli.command('bucket-objs-opts')
@click.option('--bucket-name', default=False)
def get_bucket_objs_as_opts(bucket_name):
    "Get bucket objects"
    for obj in bucket_mgr.all_objs(bucket_name):
        print(obj)


@cli.command('bucket-objs')
@click.argument('bucket_name')
def get_bucket_objs(bucket_name):
    """Get bucket objects."""
    for obj in bucket_mgr.all_objs(bucket_name):
        print(obj)


#s3_bucket = s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': session.region_name})
@cli.command('setup_bucket')
@click.argument('bucket_name')
def setup_bucket(bucket_name):
    """Create and configure s3 bucket."""
    bucket = bucket_mgr.init_bucket(bucket_name)
    bucket_mgr.set_policy(bucket)
    url = bucket_mgr.config_website(bucket, "index.html", "err.html")
    print(url)   


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket_name')
def sync(pathname, bucket_name):
    """Sync contents of PATHNAME to BUCKET."""
    bucket_mgr.sync(pathname, bucket_name)

if __name__ == '__main__':
    cli()
