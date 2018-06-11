from __future__ import print_function
import json
from datetime import datetime
import boto3
print('Loading function')
def lambda_handler(event, context):
    try:
        job_id = event['CodePipeline.job']['id']
    except KeyError as err:
        LOGGER.error("Could not retrieve CodePipeline Job ID!\n%s", err)
        return False
    print("Received event: " + json.dumps(event, indent=2))
    #print("value1 = " + event['key1'])
    #print("value2 = " + event['key2'])
    #print("value3 = " + event['key3'])
    print("Almost there!")
    print("Dammit, this better work! NOW!!!")
    print("All that this needs is documentation!")
    print(str(datetime.now()))
    #return event['key1']  # Echo back the first key value
    return "Success"
    try:
        codepipeline = boto3.client('codepipeline')
        codepipeline.put_job_success_result(jobId=job_id)
        LOGGER.info('===SUCCESS===')
        return True
    except ClientError as err:
        LOGGER.error("Failed to PutJobSuccessResult for CodePipeline!\n%s", err)
        return False
