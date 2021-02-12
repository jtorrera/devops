import os
import json
import boto3
from types import SimpleNamespace
from todos import decimalencoder

translate_client = boto3.client('translate')

dynamodb = boto3.resource('dynamodb')

def get(event, context):
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    language = event['pathParameters']['language']

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    

    result_dict = json.dumps(result['Item'],  cls=decimalencoder.DecimalEncoder)
    
    # Parse JSON into an object
    todo = json.loads(result_dict, object_hook=lambda d: SimpleNamespace(**d))

    # Translate text with Source Language auto detect
    result = translate_client.translate_text(Text = todo.text, SourceLanguageCode="auto", TargetLanguageCode=language)
    
    # create a response
    response = {
        "statusCode": 200,
        "body": "[ Text : " + todo.text + " - Languaje : " + language + " - Translation : " + result['TranslatedText'] + " ] "
    }

    return response
    