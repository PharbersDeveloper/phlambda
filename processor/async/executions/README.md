# create pharbers trigger state machine factory

```
aws cloudformation create-stack --stack-name pharbers-trigger --template-body file://steps-cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/factory-sm.json ParameterKey=StateMachineName,ParameterValue=pharbers-trigger
```


# create debug step function via cloud formation

```
aws cloudformation create-stack --stack-name alfredtestv1 --template-body file://steps-cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/FirstSM.json
```


```
aws cloudformation create-stack --stack-name alfredtestv1 --template-body file://steps-cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/alfred-step-function-runnerId.json
```
