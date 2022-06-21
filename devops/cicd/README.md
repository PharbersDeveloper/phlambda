# create resource creating state machine factory

```
aws cloudformation create-stack --stack-name phtestcodebuild --template-body file://lmdandsfn.yaml --parameters ParameterKey=SubmitOwner,ParameterValue=hbzhao ParameterKey=S3Bucket,ParameterValue=ph-platform ParameterKey=S3TemplateKey,ParameterValue=2020-11-11/cicd/deprecated/phtestcodebuild/sm.json ParameterKey=StateMachineName,ParameterValue=phtestcodebuild --capabilities CAPABILITY_AUTO_EXPAND
```

--capabilities CAPABILITY_AUTO_EXPAND