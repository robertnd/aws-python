import boto3
import click

session = boto3.Session(profile_name='admin')
s3 = session.resource('s3')
s3c = session.client('s3')

@click.group()
def cli():
    pass

@cli.command('list-buckets')
def listbuckets():
    "List buckets in AWS accounts"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('bucket-objs')
@click.option('--bucket-name', default=False)
def get_bucket_objs(bucket_name):
    "Get bucket objects"
    for obj in s3.Bucket(bucket_name).objects.all():
        print(obj)

if __name__ == '__main__':
    cli()
