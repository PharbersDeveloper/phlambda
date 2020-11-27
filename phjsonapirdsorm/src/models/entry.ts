import * as fortune from "fortune"
import {  logger, redis} from "phnodelayer"

class Entry {
    public model: any = {
        asset: {
            name: String,
            block: { link: "dataBlock", isArray: true, inverse: "assetBlock" },
            owner: String,
            extension: String,
            size: Number,
            source: String,
            type: String, // candidate: database, file, stream, application, mart, cube
            accessibility: String,
            version: String,
            isNewVersion: Boolean,
            shared: String, // null => 未公开, Access => 公开成功, Applying => 审核正在公开中
            parthers: String, // 对应公司ID
            providers: Array(String),
            markets: Array(String),
            molecules: Array(String),
            dateCover: Array(String),
            geoCover: Array(String),
            labels: Array(String),
            created: Date,
            modified: Date,
            description: String,
        },
        dataBlock: {
            assetBlock: {link: "asset", inverse: "block"},
            dfs: {link: "dataSet", isArray: true, inverse: "blockDs"},
            name: String,
            label: String,
            startRow: Number,
            type: String,
            description: String,
        },
        dataSet: {
            parent: { link: "dataSet", isArray: true, inverse: "child" },
            child: { link: "dataSet", isArray: true, inverse: "parent" },
            blockDs: { link: "dataBlock", inverse: "dfs" },
            sampleData: {link: "dataSetSample", isArray: true, inverse: "ds"},
            job: { link: "job", inverse: "gen" },
            name: String,
            schema: Array(String),
            source: String,
            storeType: String,
            size: Number,
            created: Date,
            modified: Date,
            description: String,
        },
        dataSetSample: {
            ds: {link: "dataSet", inverse: "sampleData"},
            data: String,
            created: Date,
            modified: Date,
            description: String,
        },
        job: {
            gen: { link: "dataSet", isArray: true, inverse: "job" },
            task: String,
            inputDS: Array(String),
            outPutDS: Array(String),
            jobId: String,
            asset: String,
            status: String,
            start: Date,
            end: Date,
            created: Date,
            modified: Date,
            description: String,
        },
        // dbSource: {
        //     dbType: String,
        //     url: String,
        //     user: String,
        //     pwd: String,
        //     dbName: String,
        //     create: Date,
        //     assetDbs: { link: "asset", inverse: "dbs" }
        // },
    }

    public operations = {
        hooks: {
            asset: [ this.hooksDate, this.output ],
            dataSet: [ this.hooksDate ],
            dataSetSample: [ this.hooksDate ],
            job: [ this.hooksDate ]
        }
    }

    protected hooksDate(context, record, update) {
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
                update.replace.modified = new Date()
                return update
        }
    }

    protected async output(context, record) {
        const { request: { method, meta: { language } } } = context
        const { errors: { BadRequestError } } = fortune
        if (method === "find") {
            // TODO：企业公开数据权限验证不是正解，
            // 这样写的原因是API Gateway的授权选择TOKEN类型捕捉不到后续过滤参数，
            // 经查询AWS文档应改为REQUEST类型，并将所有Lambda的验证授权改为此，此问题将记录jira
            const rds: any = redis.getInstance
            try {
                if (rds.store.connectionStatus === 0) {
                    await rds.open()
                }
                // tslint:disable-next-line:max-line-length
                const res = await rds.find("access", null, {match: {token: context.request.meta.request.rawHeaders.Authorization}})
                if (res.payload.records.length === 0) {
                    throw new BadRequestError("token is null")
                }
                const scope = res.payload.records[0].scope
                // tslint:disable-next-line:max-line-length
                // "APP|entry:assets&filter[parthers]=1:*:R,entry:assets&filter[owner]=222:*:W|W#APP|phcommon:accounts:aaa:W,phcommon:parthers:bbb:R|W"
                if (scope === "*") {
                    return
                }
                const oauthScope = scope.split("#").find((item) => item.includes("entry"))
                const entryScope = oauthScope.split("|")[1].split(",")
                if (entryScope.length === 1 && entryScope[0] === "*") {
                    return
                }
                const resourceType = context.request.uriObject.type
                const queryStr = context.request.meta.request.queryStr.split("&").
                map((item) => `${resourceType}&${item}`)
                const flags = entryScope.map((item) => {
                    if (item.split(":")[1].includes("&")) {
                        return queryStr.includes(item.split(":")[1])
                    } else {
                        return true
                    }
                })
                if (!flags.includes(true)) {
                    throw new BadRequestError("unauthorized")
                }
            } catch (e) {
                throw e
            }
        }
        return record
    }
}

export default Entry
