import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    
    queryStringParameters = event['queryStringParameters']
    deviceID = queryStringParameters['deviceID']
    
    AuthResponse = checkAuthData(event, context, deviceID)
    
    if AuthResponse:
        response = {'status': 'Success', 'message': 'You have successfully logged in'}
    else:
        postRegistrationData(event, context, deviceID)
        response = {'status': 'Success', 'message': 'New account successfully created'}

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
    
def checkAuthData(event, context, deviceID):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DB_Devices')
    
    responseTable = table.query(KeyConditionExpression=Key('device_id').eq(deviceID))
    
    if len(responseTable['Items']) > 0:
        return True
    else:
        return False
        
        
def postRegistrationData(event, context, deviceID):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DB_Devices')

    table.put_item(
        Item={
            'device_id': deviceID,
            'app_settings': 'None',
            'app_usage': 'None',
            'other': 'None',
            'premium_plan_info': 'None',
            'storage': 'None',
        }
    )
