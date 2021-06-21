
aws 请升级aws-cli 到2.0.30 + 版本
要不然没有 --file-system-configs

```
arn:aws-cn:elasticfilesystem:cn-northwest-1:444603803904:access-point/fsap-014936bda9775c1e2
aws lambda update-function-configuration --function-name PhCICDRShiny --fs-config FileSystemArn=arn:aws-cn:elasticfilesystem:cn-northwest-1:444603803904:access-point/fsap-014936bda9775c1e2,LocalMountPath=/environment
```