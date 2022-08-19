from django import template
import boto3.session

register = template.Library()
session = boto3.session.Session(region_name='us-east-1')
s3Client = session.client('s3')


@register.simple_tag(name='presign')
def presign(file):
    response = s3Client.generate_presigned_url('get_object', Params={'Bucket': 'zag-mag', 'Key': file}, ExpiresIn=3600)
    return response


@register.filter(name='to_cents')
def to_cents(value):
    return int(value * 100)


@register.filter(name='pluralize')
def pluralize(value):
    retval = ""
    if value > 1:
        retval = "s"
    return retval
