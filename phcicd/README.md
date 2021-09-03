# phlambdaCICD流程

当对phlambda进行指定的操作时，会触发webhook，通过apigateway调用lambda上传代码到s3

当s3上传code.zip后触发S3event，调用启动codebuild的lambda

#### 1.上传code.zip lambda

```
1. lambda接收bitbucket的event，解析body的内容，获取必要的信息
   主要包括，分支的操作类型、时间、操作者、repository名称、branch名称
2. 处理好信息后进行拉取代码,可以根据repository、branch等信息进行拉取代码
   拉取代码使用的是gitpython库进行git的操作
3. 拉取代码后打包代码上传到指定的s3位置 

```

 

#### 2.设置s3event

```
1. 首先创建lambda，用于启动codebulid
2. 在指定的bucket，
	· 点击事件通知下的 创建事件通知
	· 设置前缀，后缀
	· 指定事件类型
	· 设置目标为lambda函数
当有code.zip上传，就会触发S3 event执行lambda 运行codebuild
```



#### 3.创建ApiGateway

```
在apigateway创建POST方法
当触发时调用上传code.zip的lambda
```



#### 4.bitbucket的webhook

```
在bitbucket的找到repository设置webhook 
webhook的url设置为apigateway的路径，设置好指定的events
```



#### 5.CodeBuild创建

```
使用cloudformation创建codebuild
```

