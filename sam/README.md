# sam-app
sam build

sam package --profile aws-webinar  --output-template packaged.yaml --s3-bucket sagemaker-sam-cobus

sam deploy --profile aws-webinar  --template-file packaged.yaml --region eu-west-1 --capabilities CAPABILITY_IAM --stack-name SagemakerSAMStackEU

