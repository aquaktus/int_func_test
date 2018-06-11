from __future__ import print_function
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
print('Loading function')
def lambda_handler(event, context):
    try:
        job_id = event['CodePipeline.job']['id']
        print(str(datetime.now()), ":", str(job_id))
    except KeyError as err:
        print("Could not retrieve CodePipeline Job ID!\n%s", err)
    print("Received event: " + json.dumps(event, indent=2))
    try:
        codepipeline = boto3.client('codepipeline')
        codepipeline.put_job_success_result(jobId=job_id)
        print('SUCCESS: All functional tests passed')
        return True
    except ClientError as err:
        LOGGER.error("Failed to PutJobSuccessResult for CodePipeline!\n%s", err)
        return False
