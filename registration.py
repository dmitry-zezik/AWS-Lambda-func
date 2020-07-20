import json
import boto3
import os
import random
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    queryStringParameters = event['queryStringParameters']
    login = queryStringParameters['login']
    password = queryStringParameters['password']
    data = login, password

    emailIsFree = checkEmail(event, context, login)

    if emailIsFree == True:
        postRegistrationData(event, context, data)
        response = {'status': 'Success', 'message': 'You have successfully registered'}
    else:
        response = {'status': 'Error', 'message': 'Email is already in use'}        

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def checkEmail(event, context, login):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DB_Users')

    responseTable = table.query(KeyConditionExpression=Key('user_login').eq(login))

    if len(responseTable['Items']) > 0:
        if responseTable['Items'][0]['confirmed'] == False:
            # no need to delete old reg data
            return True
        else:
            return False
    else:
        return True

def postRegistrationData(event, context, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('DB_Users')
    confirmation_code = random.randint(1000,9999)
    security_data = {'confirmation_code': confirmation_code}
    
    table.put_item(
        Item={
            'user_login': data[0],
            'user_password': data[1],
            'app_usage': 'None',
            'premium_plan_info': 'None',
            'app_settings': 'None',
            'security': security_data,
            'storage': 'None',
            'other': 'None',
            'confirmed': False
        }
    )
    
    #confirmEmail(confirmation_code, data[0]) 
    # THIS IS NOT READY YET


def confirmEmail(confirmation_code, email_adr):
    client = boto3.client("ses")

    subject = "Confirm email"
    body = """
        <br>
        Your confirmation code is {}.
        If you did NOT request to verify this email address, ignore this email. 
    """.format(confirmation_code)

    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}

    mail_response = client.send_email(Source = "getstuff.testuser@gmail.com",
    Destination = {"ToAddresses": [email_adr]}, Message = message)