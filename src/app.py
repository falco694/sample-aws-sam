import json
import os

import boto3


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        # api-gateway-simple-proxy-for-lambda-input-format
        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    # 認証情報不要の処理
    regions = boto3.Session().get_available_regions('ec2')
    print(regions)

    response = {}
    response["isBase64Encoded"] = False
    response["statusCode"] = 200
    response["headers"] = {}
    response["body"] = {}
    response["body"]["message"] = "ok"
    response["body"]["regions"] = regions

    return json.dumps(response)


def get_parameters(param_key):
    """ Function for get_parameters
    """
    region_name = boto3.session.Session().region_name
    ssm = boto3.client('ssm', region_name=region_name)
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']
