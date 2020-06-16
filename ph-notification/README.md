## ph-notification 
***基于 AWS-SQSEvent 的 Pharbers 通知类 Lambda 函数***

#### 前言
利用lambda-layer和go-plugin来完成可插拔的应用。
参考 [Medium blog](https://medium.com/nordcloud-engineering/how-to-build-pluggable-golang-application-and-benefit-from-aws-lambda-layers-154c8117df9b)

#### AWS Lambda 层
`您可以将 Lambda 函数配置为以层的形式拉入其他代码和内容。层是包含库、自定义运行时或其他依赖项的 ZIP 存档。利用层，您可以在函数中使用库，而不必将库包含在部署程序包中。`

#### Go plugin 简介
`A plugin is a Go main package with exported functions and variables that has been built with: go build -buildmode=plugin.`

`Plugin插件是包含可导出(可访问)的function和变量的main package编译(go build -buildmode=plugin)之后的文件。`

#### Go plugin 应用场景
1. 通过plugin我们可以很方便的对于不同功能加载相应的模块并调用相关的模块；
2. 针对不同语言(英文、汉语、德语……)加载不同的语言so文件,进行不同的输出；
3. 编译出的文件给不同的编程语言用(如：c/java/python/lua等).
4. 需要加密的核心算法,核心业务逻辑可以可以编译成plugin插件
5. 黑客预留的后门backdoor可以使用plugin
6. 函数集动态加载

#### ph-notificaton 开发约定
为方便使用SQSEvent调用，我们在处理SQSEvent时根据"ReceiptHandle"的值来决定使用哪个plugin进行处理。

所以在编写指定功能的plugin时，plugin要实现以"功能名+Handle"为命名的函数`func(events.SQSMessage) error`，build -o时指定输出以"功能名+Handle+.so"为名字的文件。

#### Build
###### 编译main函数和plugin (ps：我在mac上编译会有一些问题，尚未解决，放在linux上可以成功编译)
```shell script
$ env GOOS=linux GOARCH=amd64 CGO_ENABLED=1 go build -o main
$ env GOOS=linux GOARCH=amd64 CGO_ENABLED=1 go build -v -buildmode=plugin -o plugin/SendEmailHandle.so plugin/SendEmailHandle.go
```

#### Package
###### 将可执行的main和.so文件分别打包进lambda-function.zip和lambda-layer.zip
###### (ps：打包main和.so文件时，不能有目录，只能直接打包进去，而且aws-lambda-layer目前尝试只能识别"/opt/"目录下的文件，**不包括子目录**)
```shell script
$ zip phlambda-function-ph-notification.zip main
$ zip phlambda-layer-ph-notification.zip SendEmailHandle.so
```

#### Deploy
创建AWS-Lambda的Function和Layer，以及AWS角色和SQS触发器，就不多叙述了，使用ph-lambda自动化发布。

