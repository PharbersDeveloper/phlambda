# Pharbers AWS Lambda Auth Layer

*只适用于Pharbers公司逻辑的Auth验证逻辑*

> **后续会考虑变为开源公用接口**

## 使用说明
在AWS Lambda中添加该Layer即可使用权限验证接口
```ts
import {Errors2response, identify} from phauthlayer
// event为Lambda request
// scope为字符串
// flag为object
const flag = identify.identify(event, scope)
console.info(typeof flag)
console.info(flag)
```

