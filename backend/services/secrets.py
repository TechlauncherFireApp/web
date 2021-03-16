import json

import boto3
import base64
from botocore.exceptions import ClientError


class SecretService:
    secret = {}
    secret_name = ''
    region_name = ''

    def __init__(self, secret_name, region_name="ap-southeast-2"):
        self.secret_name = secret_name
        self.region_name = region_name

    def get(self):
        # Only retrieve if not retrieved
        if self.secret != {}:
            return self.secret

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                self.secret = json.loads(secret)
                return self.secret
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                # Not sure how to handle
