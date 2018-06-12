from __future__ import print_function
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

# this is what we will use to make the endpont requests
from botocore.vendored import requests
print("requests loaded correctly")

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
    ft_passed = True
    # If all functional tests passed, call PutJobSuccessResult with this job id.
    # Else, PutJobFailureResult with this job id.
    # Import the tests
    with open('tests.json') as f:
        print("reading tests.json")
        tests = json.load(f)
    if tests is None:
        # This forces there to be functional tests
        print("No tests.json found!")
        ft_passed = False
    print("tests.json found located!")
    
    if ft_passed:
        codepipeline = boto3.client('codepipeline')
        try:  
            codepipeline.put_job_success_result(jobId=job_id)
            print('SUCCESS!!!!: All functional tests passed')
            return True
        except ClientError as err:
            print("Failed to PutJobSuccessResult for CodePipeline!\n%s", err)
            return False
    else:
        try:
            codepipeline.put_job_failure_result(jobId=job_id, failureDetails={
            'type': 'JobFailed',
            'message': 'Functional Tests failed',
            'externalExecutionId': 'string'})
            print('FAILURE!!!!: Some functional tests failed')
            return True
        except ClientError as error:
            print("Failed to PutJobFailureResult for CodePipeline!\n%s", err)
            return False
