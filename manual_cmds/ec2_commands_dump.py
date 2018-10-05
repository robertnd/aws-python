# coding: utf-8
import boto3
import os, stat

session = boto3.Session(profile_name='admin')
ec2 = session.resource('ec2')

key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material

with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
get_ipython().run_line_magic('ls', '-l')

os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')

imags = ec2.images.filter(Owners=['amazon'])

for img in imags:
    print(img)
img = ec2.Image('ami-0ff8a91507f77f867')

img.description
img.name
ami_name = img.name

filters = [{'Name':'name', 'Values': [ami_name]}]
list(ec2.images.filter(Owners=['amazon'], Filters=filters))

instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1,InstanceType='t2.micro',KeyName=key.key_name)

inst = instances[0]
inst.reload()
inst.public_dns_name
inst.security_groups
inst.security_groups[0]['GroupName']
inst.security_groups[0]['GroupId']
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])

sg.authorize_ingress(IpPermissions=[{'FromPort':22, 'ToPort':22, 'IpProtocol':'TCP', 'IpRanges':[{'CidrIp':'0.0.0.0/0'}]}])

