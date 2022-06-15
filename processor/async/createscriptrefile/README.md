# create resource creating state machine factory

```
aws cloudformation create-stack --stack-name create-script-file-sfn --template-body file://cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-platform ParameterKey=S3TemplateKey,ParameterValue=2020-11-11/jobs/statemachine/pharbers/template/sm.json ParameterKey=StateMachineName,ParameterValue=create-script-file
```
