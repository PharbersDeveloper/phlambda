# Pharbers AWS Lambda Layer

简化前端逻辑层的使用方式，屏蔽底层接口与逻辑，只需要配置model与yaml即可实现接口协议为JSONAPI功能

## 安装说明
1. npm install phnodelayer or yarn add phnodelayer
2. 安装完成后运行 npm run build or yarn run build
3. 在项目中的config目录中添加yml与log4js的配置文件
4. 在项目中的src目录中添加model
5. npm run build 编译 

## 具体使用
``src/config/server.yml``
```yaml
project: "test"
postgres:
  algorithm: postgres
  host: 127.0.0.1
  port: 5432
  username: "postgres"
  pwd: "faiz"
  dbName: "phtest"
#mongo:
#  algorithm: mongodb+srv
#  host: 127.0.0.1
#  port: 27017
#  username: "pharbers"
#  pwd: "Pharbers.84244216"
#  coll: "phtest"
#  authSource: "admin"
#  other: "?retryWrites=true&w=majority"
#  auth: true
#mysql:
#  algorithm: mysql
#  host: 127.0.0.1
#  port: 3306
#  username: "root"
#  pwd: "pharbers"
#  dbName: "phtest"
#redis:
#  dao: "test"
#  algorithm: redis
#  host: 127.0.0.1
#  port: 6379
#  db: 0
```

``src/delegate/appLambdaDelegate.ts``
```ts
import { Main } from "phnodelayer"

export default class AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        return await Main(event)
    }
}
```

``src/models/test.ts``
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

``src/app.js``
```js
let response;

const delegate = require("./dist/delegate/appLambdaDelegate").default

const app = new delegate()

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
        let result

        if (context && context.callbackWaitsForEmptyEventLoop) {
            context.callbackWaitsForEmptyEventLoop = false
        }

        result = await app.exec(event)
        response = {
            'statusCode': result.statusCode,
            'headers': result.output[0],
            'body': String(result.output[1])
        }

        const resultOutput = result.output[0].split("\r\n")
        const corsHeader =   {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PATCH,DELETE"
        }
        let objHeader = {}

        for (let index = 0; index < resultOutput.length; index++) {
            const element = resultOutput[index].split(":");
            if (element.length === 2) {
                objHeader[element[0]] = element[1]
            }
        }
        Object.assign(objHeader, corsHeader)
        response.headers = objHeader

    } catch (err) {
        return err;
    }

    return response
};

```


## Log 管理
```ts
import { logger } from "phnodelayer"

logger.trace("<what ever you want>")
logger.debug("<what ever you want>")
logger.info("<what ever you want>")
logger.warn("<what ever you want>")
logger.error("<what ever you want>")
logger.fatal("<what ever you want>")
```
