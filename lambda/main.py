import os
import boto3
import botocore

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    domain_name = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')
    connection_id = event.get('requestContext',{}).get('connectionId')
    result = connections.put_item(Item={ 'id': connection_id })

    apigw_management = boto3.client('apigatewaymanagementapi',
                            endpoint_url=F"https://4pt7sawhd9.execute-api.ap-northeast-2.amazonaws.com/demo")
    ret = "hello world";

    try:
      _ = apigw_management.post_to_connection(ConnectionId=connection_id,
                                             Data=ret)
    except botocore.exceptions.ClientError as e:
      print(e);
      return { 'statusCode': 500,
                    'body': 'something went wrong' }

    return { 'statusCode': 200,
             "body": 'connected'};