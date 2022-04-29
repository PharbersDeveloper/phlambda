# create pharbers currently project reboot

```
aws cloudformation create-stack --stack-name tenant-reboot --template-body file://steps-cfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=alfred ParameterKey=S3Bucket,ParameterValue=ph-max-auto ParameterKey=S3TemplateKey,ParameterValue=2020-08-11/reboot-sm.json ParameterKey=StateMachineName,ParameterValue=tenant-reboot
```
