# create pharbers currently project reboot

```
aws cloudformation create-stack --stack-name tenant-boot --template-body file://cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/sm.json ParameterKey=StateMachineName,ParameterValue=tenant-boot
```

```
aws cloudformation create-stack --stack-name tenant-boot-test --template-body file://cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/sm.json ParameterKey=StateMachineName,ParameterValue=tenant-boot-test
```
