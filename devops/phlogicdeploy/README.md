# lambda 创建于更新路径

## args

```
event = {

}
```

1. create lambda

```
aws lambda create-function --function-name <function-name> --runtime <python3.8 | nodejs12.x> --role <Ph-Back-RW | Ph-Data-Resource-Admin> --handler main.lambda_handler
```

2. reset code

这个地方分几个步骤：
- 第一步绑定 git repo 的 efs
- 第二步 link git repo 的编译文件
- 第三步 编译
- 第四步 编译将编译后的文件放到指定地方

> lambda, apigateway, db, sm, layer, 包括前端等并绑定版本

> 这里还需要清理并整理所有的lambda，意思是全部删除

```
aws lambda update-function-code --function-name <function-name> 
```

零时，走线下zip
发布走线上 s3


3. 还是需要数据库管理发布数据

Schema |-
	- projectName: (PartitionKey::String)
	- id: (SortKey::String)
	- ctype: (lambda | sm | apigateway | layer | frontend)
	- runtime
	- buildCommand: [""] 
	- archivePath: ""
	- sourcePath: ""
	- destinationPath: ""
	- environment: {}
	



