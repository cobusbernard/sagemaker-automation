from aws_cdk import (
    aws_sagemaker as sagemaker,
    aws_iam as iam,
    aws_s3 as s3,
    core
)

class SagemakerStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        role = iam.Role(
            scope=self,
            id="SageMakerDemo1",
            role_name="SageMakerDemo1",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('IAMReadOnlyAccess')
            ]
        )
        
        instance = sagemaker.CfnNotebookInstance( 
            scope=self,
            id="My instance",
            instance_type="ml.t2.large",
	        default_code_repository="https://github.com/cobusbernard/sagemaker-notebooks.git",
            role_arn=role.role_arn
        )

        bucket = s3.Bucket(
            scope=self, 
            id="sagemaker-demo-cobus", 
            bucket_name="sagemaker-demo-cobus"
        )

app = core.App()
SagemakerStack(app, "SagemakerStackUS", env={'region': 'us-east-1'})
SagemakerStack(app, "SagemakerStackEU", env={'region': 'eu-west-1'})
app.synth()
