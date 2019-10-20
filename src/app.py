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

    client = boto3.client('ec2')
    instance_list = client.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": [
                    "pending",
                    "running",
                    "shutting-down",
                    "terminated",
                    "stopping",
                    "stopped"
                ]
            }
        ]
    )

    output_instance_list = []
    for Reservations in instance_list["Reservations"]:
        for dev_instances in Reservations["Instances"]:
            output_instance = {}
            output_instance["instance_id"] = dev_instances["InstanceId"]
            output_instance["public_ip"] = dev_instances["PublicIpAddress"]
            output_instance["State"] = dev_instances["State"]["Name"]
            for tagitem in dev_instances["Tags"]:
                if tagitem["Key"] == "Name":
                    output_instance["instance_name"] = tagitem["Value"]

            output_instance_list.append(output_instance)

    result = ""
    for item in output_instance_list:
        result += "[{}] {} ({}) Public IP: {}\n".format(
            item["State"],
            item["instance_id"],
            item["instance_name"],
            item["public_ip"]
        )

    print(result)

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': '{"message": "ok"}'
    }


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
