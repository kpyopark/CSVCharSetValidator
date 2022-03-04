import smart_open
import io
import json
import urllib.parse
import codecs
import boto3

# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        line_stream = codecs.getreader("utf-8")
        s3_target_url =  's3://' + bucket + '/refined/' + key
        with smart_open.smart_open(s3_target_url, 'w') as fout:
            for line in line_stream(response['Body'], errors='ignore'):
                fout.write(line)
        return {
            "status" : 200,
            "target" : s3_target_url
        }
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        

