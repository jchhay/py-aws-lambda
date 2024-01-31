# Tagging Process
# EC2 creation triggers event rule
# EventBridge captures the event to trigger Lambda
# Lambda will add user tag to EC2 instance

# Setup
# Create CloudTrail trail
# Create EventBridge rule to detect 'CloudTrail' event type with operation 'RunInstances' from EC2
# Select lambda as the target of the EventBridge rule
# Ensure lambda execution role has permission to add user tags to EC2 instances

import boto3
import json

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Get the instance ID from the event
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    
    # Get the user tag from the event
    user_tag = event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']
    
    # Add the user tag to the instance
    ec2.create_tags(Resources=[instance_id], Tags=[{'Key': 'User', 'Value': user_tag}])
    
    # Return a success message
    return {
        'statusCode': 200,
        'body': json.dumps('User tag added to EC2 instance')
    }