# This code is a sample only. Not for use in production.
#
# Author: Katreena Mullican
# Contact: mullicak@amazon.com
#
import boto3
import os
import json
from decimal import Decimal
from datetime import datetime
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def handler(event, context):
    dt_request = Decimal(int(datetime.timestamp(datetime.now())))
    bucket_name = (os.environ['BUCKET_NAME'])
    key = event['Records'][0]['s3']['object']['key']
    image = {
        'S3Object': {
            'Bucket': bucket_name,
            'Name': key
        }
    }

    try:
        # Calls Amazon Rekognition DetectLabels API to classify images in S3
        response = rekognition.detect_protective_equipment(Image=image,
                                                          SummarizationAttributes={
                                                              "MinConfidence":0.6,
                                                              "RequiredEquipmentTypes":['FACE_COVER','HAND_COVER','HEAD_COVER']})

        # # Write results to JSON file in bucket results folder
        json_labels = json.dumps(response["Persons"])
        filename = os.path.basename(key)
        filename_prefix = os.path.splitext(filename)[0]
        s3.put_object(Body=json_labels, Bucket=bucket_name, Key="results/" + filename_prefix + ".json")

        # Parse the JSON for DynamoDB
        db_persons = json.loads(json_labels)
        with table.batch_writer() as batch:
            for person in db_persons:
                for body_parts in person['BodyParts']:
                    is_equipped = 1 if len(body_parts["EquipmentDetections"]) > 0 else 0
                    content = {
                        'uuid': f"{body_parts['Name']}#{is_equipped}",
                        'timestamp': dt_request,
                        'image': key,
                        'confidence': Decimal(body_parts['Confidence'])
                    }
                    batch.put_item(Item=content)
        return response

    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket_name))
        raise e