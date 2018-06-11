from __future__ import print_function
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
print('Loading function')
def lambda_handler(event, context):
    # Get the job id so that we can update the result of this lambda and codepipeline
    # can capture it
    try:
        job_id = event['CodePipeline.job']['id']
        print(str(datetime.now()), ":", str(job_id))
    except KeyError as err:
        print("Could not retrieve CodePipeline Job ID!\n%s", err)
    print("Received event: " + json.dumps(event, indent=2))
    # If all functional tests passed, call PutJobSuccessResult with this job id.
    # Else, PutJobFailureResult with this job id.
    try:
        codepipeline = boto3.client('codepipeline')
        #codepipeline.put_job_success_result(jobId=job_id)
        codepipeline.put_job_failure_result(jobId=job_id, failureDetails={
        'type': 'JobFailed',
        'message': 'Functional Tests failed',
        'externalExecutionId': 'string'})
        print('SUCCESS: All functional tests passed')
        return True
    except ClientError as err:
        LOGGER.error("Failed to PutJobSuccessResult for CodePipeline!\n%s", err)
        return False
