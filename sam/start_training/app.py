import json
import boto3, os, datetime

def lambda_handler(event, context):
    sm = boto3.client('sagemaker')
    job_names = sm.list_training_jobs(
        NameContains='xgboost-2019-09-10',
        StatusEquals='Completed',
        SortBy='CreationTime',
        SortOrder='Descending'
    )

    #job = sm.describe_training_job(TrainingJobName=training_job_name)
    job = sm.describe_training_job(job_names.TrainingJobSummaries[0].TrainingJobName)

    training_job_prefix = os.environ['xgboost']
    training_job_name = training_job_prefix+str(datetime.datetime.today()).replace(' ', '-').replace(':', '-').rsplit('.')[0]
    job['ResourceConfig']['InstanceType'] = os.environ['instance_type']
    job['ResourceConfig']['InstanceCount'] = int(os.environ['instance_count'])

    print("Starting training job %s" % training_job_name)

    if 'VpcConfig' in job:
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'], RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'], StoppingCondition=job['StoppingCondition'],
            HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else {},
            VpcConfig=job['VpcConfig'],
            Tags=job['Tags'] if 'Tags' in job else [])
    else:
        # Because VpcConfig cannot be empty like HyperParameters or Tags :-/
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'], RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'], StoppingCondition=job['StoppingCondition'],
            HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else {},
            Tags=job['Tags'] if 'Tags' in job else [])

    print(resp)


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
