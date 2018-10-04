import boto3
import click
from botocore.exceptions import ClientError

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

#s3_bucket = s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': session.region_name})
@cli.command('setup_bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "create and configure s3 bucket"
    s3_bucket = None
    errormsg = "No errors"
    try:
        s3_bucket = s3.create_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            errormsg = e.response 
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e
    
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
    """ % s3_bucket.name
    policy = policy.strip()
    policy_obj = s3_bucket.Policy()
    policy_obj.put(Policy=policy)

    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={'ErrorDocument': {'Key': 'err.html'}, 'IndexDocument': {'Suffix': 'index.html'}})
    url = "http://%s.s3-website.%s.amazonaws.com" % (s3_bucket.name, session.region_name)

    #upload file
    #s3_bucket.upload_file('samplesite/index.html', 'index.html', ExtraArgs={'ContentType': 'text/html'} )
    print(url + "\n" + errormsg)
    return

if __name__ == '__main__':
    cli()
