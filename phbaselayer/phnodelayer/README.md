# Pharbers AWS Lambda Layer

*简化前端逻辑层的使用方式，屏蔽底层接口与逻辑，只需要配置MODEL即可实现接口协议为JSONAPI功能*

> **本库目前支持POSTGRESQL、REDIS，后续会增加MYSQL、MONGODB**

## 安装说明
1. npm install phnodelayer or yarn add phnodelayer
2. 安装完成后运行 npm run build or yarn run build
3. 在项目中的src目录中添加model
4. npm run build 编译

## 具体使用

`src/delegate/appLambdaDelegate.ts`
```ts
import { ConfigRegistered, Main, PostgresConfig } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
            const pg = new PostgresConfig("Test", "postgres", "faiz", "127.0.0.1", 5432, "phtest")
            ConfigRegistered.getInstance.registered(pg)
            return await Main(event)
        }
}
```

`src/models/test.ts`
```ts
class Test {
    public model: any = {
        asset: {
            name: String,
            block: { link: "dataBlock", isArray: true, inverse: "assetBlock" },
            type: String, // candidate: database, file, stream, application, mart, cube
            created: Date,
            modified: Date,
            description: String,
        },
        dataBlock: {
            assetBlock: {link: "asset", inverse: "block"},
            name: String,
            label: String,
            type: String,
            description: String,
        },
    }

    public operations = { // 没有hooks可以不需要写
        hooks: {
            asset: [ this.hooksDate ],
        }
    }

    protected hooksDate(context, record, update) { // 没有hooks可以不需要写
        const { request: { method, meta: { language } } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                return record
            case "update":
                record.modified = new Date()
                return record
        }
    }
}

export default Test
```

`src/app.js`
```js

let response = {}

const corsHeader =   {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
}
const phLogger = require("phnodelayer").Logger
const delegate = require("./dist/delegate/appLambdaDelegate").default

const app = new delegate()


const formatResponse = (content) => {
    let objHeader = {}
    response.statusCode = content.statusCode
    response.headers = content.output[0]
    response.body = String(content.output[1])

    const resultOutput = content.output[0].split("\r\n")
    for (let index = 0; index < resultOutput.length; index++) {
        const element = resultOutput[index].split(":");
        if (element.length === 2) {
            objHeader[element[0]] = element[1]
        }
    }

    Object.assign(objHeader, corsHeader)
    response.headers = objHeader
}
/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */
exports.lambdaHandler = async function (event, context) {
    try {
        if (context && context.callbackWaitsForEmptyEventLoop) {
            context.callbackWaitsForEmptyEventLoop = false
        }
        if ( !event.body ) {
            event.body = ""
        }
        const result = await app.exec(event)
        if (result) {
            formatResponse(result)
        }

    } catch (err) {
        if ("meta" in err) {
            formatResponse(err.meta.response)
        } else {
            phLogger.error(err);
            return err;
        }
    }

    return response
};

```

## 暴露出的Config接口
```ts
import { ConfigRegistered, PostgresConfig, RedisConfig } from "phnodelayer"
```
### Interface ConfigRegistered
> 该接口只负责注册配置项并形成单例

#### 使用方法
```ts
// config参数为 暴露出的Config接口
import { ConfigRegistered } from "phnodelayer"
ConfigRegistered.getInstance.registered(config)

```
### Interface PostgresConfig
> 该接口只负责初始化Postgresql的链接参数

#### 使用方法
```ts
import { PostgresConfig } from "phnodelayer"
const pg = new PostgresConfig("entry", "userName", "password", "host", port , "dbName")
```

### Interface RedisConfig
> 该接口只负责初始化Redis的链接参数

#### 使用方法
```ts
import { RedisConfig } from "phnodelayer"
const redis = new RedisConfig("entry", "userName", "password", "host", port, "dbName")
```
### Interface SF
> 该接口负责暴露已存在的Store初始化实例

#### 使用方法
```ts
import {  SF, Store } from "phnodelayer"
// 如需要获取Redis实例
const rds: any = SF.getInstance.get(Store.Redis)
rds.open()
rds.close()
```

## Log 管理
```ts
import { Logger } from "phnodelayer"

Logger.trace("<what ever you want>")
Logger.debug("<what ever you want>")
Logger.info("<what ever you want>")
Logger.warn("<what ever you want>")
Logger.error("<what ever you want>")
Logger.fatal("<what ever you want>")
```