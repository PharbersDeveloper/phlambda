# create resource creating state machine factory

```
aws cloudformation create-stack --stack-name change-reosurce-position-sfn --template-body file://cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=hbzhao ParameterKey=S3Bucket,ParameterValue=ph-platform ParameterKey=S3TemplateKey,ParameterValue=2020-11-11/jobs/statemachine/pharbers/template/sm.json ParameterKey=StateMachineName,ParameterValue=change-reosurce-position
```
