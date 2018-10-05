import boto3   
import os, stat

"""Getting resources.""" 
s3 = boto3.resource('s3')
ec2 = session.resource('ec2')


#S3=====================================================================================================================
bucket.objects.all().delete() #delete all buckets --or
for obj in bucket.objects.all():
    obj.delete()

bucket = s3.Bucket('my-bucket') #get a bucket


#EC2=====================================================================================================================
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)

with open(key_path, 'w') as key_file: #write to file
    key_file.write(key.key_material)


os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR) #change key perms

ec2.images.filter(Owners=['amazon']) 
imags = ec2.images.filter(Owners=['amazon']) #filter AMIs
img = ec2.Image('ami-0ff8a91507f77f867') # Get image

ami_name = img.name #return image name (same in all regions, even if img ID changes region to region)
filters = [{'Name':'name', 'Values': [ami_name]}] #Create Filter
list(ec2.images.filter(Owners=['amazon'], Filters=filters))

#create instances
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1,InstanceType='t2.micro',KeyName=key.key_name)


#Raw AWS CLI===========================================================================================================
#Delete bucket files:
    aws s3 rm s3://<bucket> --recursive

#Delete bucket:
    aws s3 rb s3://<bucket>