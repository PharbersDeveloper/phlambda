import axios from "axios"
import fortune from "fortune"
import * as fs from "fs"
import {JsonConvert} from "json2typescript"
import { v4 as uuidv4 } from "uuid"
import phLogger from "../logger/phLogger"
import {OssTask} from "../models/ossTask"
import AppLambdaDelegate from "./appLambdaDelegate"

const kafkaRestfulUrl = "http://192.168.96.159:30082/topics"
const callAirFlow = "http://192.168.62.76:30086/api/experimental/dags/create_hive_table/dag_runs"

// TODO: 先将原来的代码翻译过来
export default class AppLambdaScheduleDelegate extends AppLambdaDelegate {

    public redisStore: any

    public async exec(event: Map<string, any>) {
        const entryEvent =  JSON.parse(String(fs.readFileSync("config/event_entry.json", "utf8")))
        // @ts-ignore
        if (event.Records.length > 0) {
            // @ts-ignore
            switch (event.Records[0].messageAttributes.type.stringValue) {
                case "PushJob" :
                    // @ts-ignore
                    await this.PushJob(event.Records[0].body, entryEvent)
                    break
                case "PushDs":
                    // @ts-ignore
                    await this.PushDS(event.Records[0].body, entryEvent)
                    break
                case "SetMartTags":
                    // @ts-ignore
                    await this.SetMartTags(event.Records[0].body, entryEvent)
                    break
                case "AssetDataMart":
                    // @ts-ignore
                    await this.AssetDataMart(event.Records[0].body, entryEvent)
                    break
                case "SandBoxDataSet":
                    // @ts-ignore
                    await this.SandBoxDataSet(event.Records[0].body, entryEvent)
                    break
                case "UpdateVersion":
                    // @ts-ignore
                    await this.UpdateVersion(event.Records[0].body, entryEvent)
                    break
                default:
                    // @ts-ignore
                    phLogger.info(event.Records[0].messageAttributes.type.stringValue)
                    phLogger.info("is not implementation")
                    break
            }
        }

        return null
    }

    public async prepare() {
        await super.prepare()
        const record = this.genTokenRecord()
        const adapter = this.genRedisAdapter()
        this.redisStore = fortune(record, {adapter})
        await this.redisStore.connect()
    }

    protected genTokenRecord() {
        const filename = "../models/redis.js"
        return require(filename).default
    }

    protected genEvent(method: string, type: string, path: string, body: any, event: Map<string, any>) {
        // @ts-ignore
        event.path = `/schedule/${type}${path}`
        // @ts-ignore
        event.httpMethod = method
        // @ts-ignore
        event.pathParameters.type = type
        // @ts-ignore
        event.requestContext.path = event.path
        // @ts-ignore
        event.requestContext.httpMethod = method
        // @ts-ignore
        event.body = body === "" ? "" : JSON.stringify(body)
        return event
    }

    private async PushJob(data: any, event: Map<string, any>) {
        // 1 create job 2 create dataset将关联关系带进去 3 update asset dfs 4 给kafka proxy send message
        const jsonConvert: JsonConvert = new JsonConvert()
        // tslint:disable-next-line:max-line-length
        const ossTask = typeof data === "string" ? jsonConvert.deserializeObject(JSON.parse(data), OssTask) : jsonConvert.deserializeObject(data, OssTask)
        const schemaJobId = `schema_job_${uuidv4()}`
        const param = {
            parent: [],
            jobId: schemaJobId,
            description: "schemaJob"
        }
        const schemaJob = await this.InitJob(param, event)
        param.parent =  param.parent.concat(schemaJob.id)
        param.jobId = `clean_job_${uuidv4()}`
        param.description = `pyJob`
        const pythonJob = await this.InitJob(param, event)
        await this.updateDfs(ossTask.assetId, schemaJob, pythonJob, event)
        ossTask.jobId = schemaJobId

        const jsonObject = jsonConvert.serializeObject(ossTask)
        const jsonObjectKeys = Object.keys(jsonObject)
        const json2LowerCaseObject = {}
        for (const key of jsonObjectKeys) {
            json2LowerCaseObject[key.replace(/^\S/, (s) => s.toLowerCase())] = jsonObject[key]
        }

        await axios({
            method: "POST",
            url: `${kafkaRestfulUrl}/oss_task_submit`,
            data: {
                value_schema: JSON.stringify({
                    type: "record",
                    name: "OssTask",
                    namespace: "com.pharbers.kafka.schema",
                    fields: [
                        {
                            name: "assetId",
                            type: "string"
                        },
                        {
                            name: "jobId",
                            type: "string"
                        },
                        {
                            name: "traceId",
                            type: "string"
                        },
                        {
                            name: "ossKey",
                            type: "string"
                        },
                        {
                            name: "fileType",
                            type: "string"
                        },
                        {
                            name: "fileName",
                            type: "string"
                        },
                        {
                            name: "sheetName",
                            type: "string"
                        },
                        {
                            name: "owner",
                            type: "string"
                        },
                        {
                            name: "createTime",
                            type: "long"
                        },
                        {
                            name: "labels",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        },
                        {
                            name: "dataCover",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        },
                        {
                            name: "geoCover",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        },
                        {
                            name: "markets",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        },
                        {
                            name: "molecules",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        },
                        {
                            name: "providers",
                            type: {
                                items: "string",
                                type: "array"
                            }
                        }
                    ]
                }),
                records: [ { value: json2LowerCaseObject } ]
            },
            headers: {"Content-Type": "application/vnd.kafka.avro.v2+json", "Accept": "application/vnd.kafka.v2+json"}
        })
    }

    private async PushDS(data: any, event: Map<string, any>) {
        // 1. 根据参数项DS更新数据 2. 更新数据后调用下一个Job
        const jobs = {
            schemaJob: {
                next: "pyJob"
            },
            pyJob: {
                next: null
            }
        }
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const jobId = dobj.jobId
        const columnNames = dobj.columnNames
        const tabName = dobj.tabName
        const length = dobj.length
        const url = dobj.url
        const status = dobj.status

        const jobRes = await super.exec(this.genEvent(`GET`, `jobs`, `?filter[jobContainerId]=${jobId}`, "", event))
        // @ts-ignore
        const job = JSON.parse(String(jobRes.output[1]))
        const dsId = job.data.length === 1 ? job.data[0].relationships.gen.data.id : "-1"

        // 更新DS数据
        await super.exec(this.genEvent(`PATCH`, `data-sets`, `/${dsId}`, {
            data: {
                type: "data-sets",
                id: dsId,
                attributes: {
                    colNames: columnNames,
                    length,
                    url,
                    tabName,
                    status
                }
            }
        }, event))

        // 调用下一个Job
        const nextJob = jobs[dobj.description]
        if (status === "end"  && nextJob.next !== null ) {
            const dsRes = await super.exec(this.genEvent(`GET`, `data-sets`, `/${dsId}/child`, "", event))
            // @ts-ignore
            const ds = JSON.parse(String(dsRes.output[1]))
            const filterJob = ds.data.find((item) => item.attributes.description === nextJob.next)
            const nextJobRes = await super.exec(this.genEvent(`GET`, `jobs`, `/${filterJob.relationships.job.data.id}`, "", event))
            // @ts-ignore
            const next = JSON.parse(String(nextJobRes.output[1]))
            const nextJobId = next.data.attributes["job-container-id"]

            const metadataPath = `${url.substring(0, url.lastIndexOf("/"))}/metadata`

            await axios({
                method: "POST",
                url: `${kafkaRestfulUrl}/oss_msg`,
                data: {
                    value_schema: JSON.stringify({
                        type: "record",
                        name: "EventMsg",
                        namespace: "com.pharbers.kafka.schema",
                        fields: [
                            {
                                name: "jobId",
                                type: "string"
                            },
                            {
                                name: "traceId",
                                type: "string"
                            },
                            {
                                name: "type",
                                type: "string"
                            },
                            {
                                name: "data",
                                type: "string"
                            }
                        ]
                    }),
                    records: [ { value: {
                            traceId: " ",
                            jobId: nextJobId,
                            type: "Python-FileMetaData",
                            data: JSON.stringify({
                                jobId: nextJobId,
                                noticeTopic: "HiveTaskNone",
                                metadataPath,
                                filesPath: url
                            })
                        } } ]
                },
                headers: {"Content-Type": "application/vnd.kafka.avro.v2+json", "Accept": "application/vnd.kafka.v2+json"}
            })
            phLogger.info("Next Job to Python")
        } else if (status === "end"  && nextJob.next == null ) { // TODO：不改变原有逻辑（怕改错后花费时间会更多），直接开辟新的逻辑，后续重构
            phLogger.info("调用生成HIVE表")
            const tabNames = {
                "CPA&GYC": "cpa",
                "CPA&PTI&DDD&HH": "cpa",
                "GYC&CPA": "cpa",
                "GYC": "cpa",
                "CPA": "cpa",
                "CHC": "chc",
                "RESULT": "result",
                "product": "prod",
                "universe": "universe"
            }
            const assetRes = await super.exec(this.genEvent(`GET`, `data-sets`, `/${dsId}/asset-ds`, "", event))
            // @ts-ignore
            const asset = JSON.parse(String(assetRes.output[1]))
            const tbName = tabNames[asset.data.attributes.providers.pop()]
            const redisRes = await this.redisStore.adapter.redis.get(asset.data.id)
            const parm = JSON.parse(redisRes)
            const outPutPath = parm.output_path
            const outPutType = parm.output_type
            const saveMode = parm.save_mode
            const version = parm.version
            const conf = {
                input_file_format: "json",
                input_path: url,
                output_file_format: outPutType,
                output_path: `${outPutPath}/${tbName}/${version}`,
                save_mode: saveMode,
                table_name: tbName
            }

            await axios({
                method: "POST",
                url: callAirFlow,
                data: {conf: JSON.stringify(conf)},
                headers: {"Content-Type": "application/vnd.kafka.avro.v2+json", "Accept": "application/vnd.kafka.v2+json"}
            })
            await this.redisStore.disconnect()
        } else {
            return null
        }
    }

    private async AssetDataMart(data: any, event: Map<string, any>) {
        // 1. 根据asset name查询到最新Asset记录 2. 处理 append与overwrite情况 3. create DataMart记录
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const assetName = dobj.assetName
        const saveMode = dobj.saveMode
        const assetUrl = `?sort=-createTime&filter[name]=${assetName}&filter[isNewVersion]=true&page[limit]=1&page[offset]=0`
        const assetRes = await super.exec(this.genEvent(`GET`, `assets`, `${assetUrl}`, "", event))
        // @ts-ignore
        const asset = JSON.parse(String(assetRes.output[1]))
        if (asset.data.length === 0) {
            return await this.createDataMart(data, event)
        }
        switch (saveMode) {
            case "append":
                const martRes = await super.exec(this.genEvent(`GET`, `assets`, `/${asset.data[0].id}/mart`, ``, event))
                // @ts-ignore
                const mart = JSON.parse(String(martRes.output[1]))
                const dfs = dobj.dfs.map((item) => {
                    return {type: "data-sets", id: item}
                }).concat(mart.data.relationships.dfs.data)
                await super.exec(this.genEvent(`PATCH`, `marts`, `/${mart.data.id}`, {
                    data: {
                        type: "marts",
                        id: `${mart.data.id}`,
                        relationships: { dfs: { data: dfs } }
                    }
                }, event))
                break
            case "overwrite":
                await super.exec(this.genEvent(`PATCH`, `assets`, `/${asset.data[0].id}`, {
                    data: {
                        type: "assets",
                        id: `${asset.data[0].id}`,
                        attributes: { isNewVersion: false }
                    }
                }, event))
                await this.createDataMart(data, event)
                break
            default:
                phLogger.info("其他情况")
                break
        }
    }

    private async SandBoxDataSet(data: any, event: Map<string, any>) {
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const jobId = dobj.jobId
        const colNames = dobj.columnNames
        const length = dobj.length
        const url = dobj.url
        const status = dobj.status
        const jobRes = await super.exec(this.genEvent(`GET`, `jobs`, `?filter[jobContainerId]=${jobId}`, ``, event))
        // @ts-ignore
        const job = JSON.parse(String(jobRes.output[1]))
        if (job.data !== undefined && job.data.length !== 0) {
            const dsRes = await super.exec(this.genEvent(`GET`, `jobs`, `/${job.data[0].id}/gen`, ``, event))
            // @ts-ignore
            const ds = JSON.parse(String(dsRes.output[1]))
            if (ds.data !== undefined) {
                await super.exec(this.genEvent(`PATCH`, `data-sets`, `/${ds.data.id}`, {
                    data: {
                        type: "data-sets",
                        id: ds.data.id,
                        attributes: { colNames, length, url, status }
                    }
                }, event))
            } else {
                await this.createDs(data, event, job)
            }
        } else {
            await this.createDs(data, event, null)
        }
    }

    private async SetMartTags(data: any, event: Map<string, any>) {
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const assetId = dobj.assetId
        const tag = dobj.tag

        const assetRes = await super.exec(this.genEvent(`GET`, `assets`, `/${assetId}`, "", event))
        // @ts-ignore
        const asset = JSON.parse(assetRes.output[1])
        if (!asset.data.attributes["mart-tags"].includes(tag)) {
            const martTags = asset.data.attributes["mart-tags"].concat(tag)
            await super.exec(this.genEvent(`PATCH`, `assets`, `/${assetId}`,  {
                data: {
                    id: assetId,
                    type: "assets",
                    attributes: { martTags }
                }
            }, event))
        }

        phLogger.info(data)
    }

    private async UpdateVersion(data: any, event: Map<string, any>) {
        function convertVersion(version: string) {
            const nums = version.split(".")
            const lastNum = Number(nums.pop()) + 1
            return nums.concat(lastNum.toString()).join(".")
        }
        // 1、查找历史记录 2、将找到记录isNewVersion设置False 3、创建新版本记录 file asset 4、更新关联数据 fileIndex
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const assetId = dobj.assetId
        const fileUrl = dobj.fileUrl

        // 根据asset id 找到历史版本数据
        // @ts-ignore
        // tslint:disable-next-line:max-line-length
        const historyAsset = JSON.parse(String((await super.exec(this.genEvent("GET", "assets", `/${assetId}`, "", event))).output[1]))
        // @ts-ignore
        // tslint:disable-next-line:max-line-length
        const historyFile = JSON.parse(String((await super.exec(this.genEvent("GET", "assets", `/${assetId}/file`, "", event))).output[1]))
        // @ts-ignore
        // tslint:disable-next-line:max-line-length
        const fileIndex = JSON.parse(String((await super.exec(this.genEvent("GET", "file-indices", `/${historyAsset.data.relationships.fi.data.id}`, "", event))).output[1]))

        // 将历史版本设置为不可读的的版本 isNewVersion = False
        await super.exec(this.genEvent("PATCH", "assets", `/${assetId}`, {
            data: {
                type: "assets",
                id: assetId,
                attributes: {isNewVersion: false}
            }
        }, event))

        // 创建新的File记录
        // tslint:disable-next-line:max-line-length
        const extension = historyFile.data.attributes.extension === "xls" ? "xlsx" : historyFile.data.attributes.extension
        // tslint:disable-next-line:max-line-length
        const fileName = historyFile.data.attributes.extension === "xls" ? historyFile.data.attributes["file-name"].replace(".xls", ".xlsx") : historyFile.data.attributes["file-name"]

        const file = JSON.parse(String((await super.exec(this.genEvent("POST", "files", "", {
            data: {
                type: "files",
                attributes: {
                    fileName,
                    extension,
                    size: historyFile.data.attributes.size,
                    label: historyFile.data.attributes.label,
                    sheetName: historyFile.data.attributes["sheet-name"],
                    startRow: historyFile.data.attributes["start-row"],
                    url: fileUrl
                }
            }
        // @ts-ignore
        }, event))).output[1]))

        // 创建新的Asset记录
        const asset = JSON.parse(String((await super.exec(this.genEvent("POST", "assets", "", {
            data: {
                type: "assets",
                attributes: {
                    name: historyAsset.data.attributes.name,
                    owner: historyAsset.data.attributes.owner,
                    accessibility: historyAsset.data.attributes.accessibility,
                    version: convertVersion(historyAsset.data.attributes.version),
                    isNewVersion: true,
                    dataType: historyAsset.data.attributes["data-type"],
                    providers: historyAsset.data.attributes.providers,
                    markets: historyAsset.data.attributes.markets,
                    molecules: historyAsset.data.attributes.molecules,
                    dataCover: historyAsset.data.attributes["data-cover"],
                    geoCover: historyAsset.data.attributes["geo-cover"],
                    labels: historyAsset.data.attributes.labels,
                    dfs: [],
                    description: historyAsset.data.attributes.description,
                    createTime: new Date()
                },
                relationships: {
                    file: {
                        data: {
                            type: "files",
                            // @ts-ignore
                            id: file.data.id
                        }
                    }
                }
            }
        // @ts-ignore
        }, event))).output[1]))

        // 更新fileIndex关联数据
        await super.exec(this.genEvent("PATCH", "file-indices", `/${fileIndex.data.id}`, {
            data: {
                type: "file-indices",
                id: fileIndex.data.id,
                attributes: {
                    url: fileUrl,
                    extension
                },
                relationships: {
                    assets: {
                        data: fileIndex.data.relationships.assets.data.concat({
                            type: "assets",
                            id: asset.data.id
                        })
                    }
                }
            }
        }, event))
    }

    private async InitJob(data: any, event: Map<string, any>) {
        // 创建Job 记录
        const jobRes = await super.exec(this.genEvent(`POST`, `jobs`, ``, {
            data: {
                type: "jobs",
                attributes: {
                    codeProvider: "test",
                    codeRepository: "",
                    create: new Date(),
                    jobContainerId: data.jobId,
                    codeVersion: "",
                    codeBranch: "",
                    description: ""
                }
            }
        }, event))
        // @ts-ignore
        const job = JSON.parse(String(jobRes.output[1]))
        const dsRes = await super.exec(this.genEvent(`POST`, `data-sets`, ``, {
            data: {
                type: "data-sets",
                attributes: {
                    colNames: [],
                    length: 0,
                    url: "",
                    description: data.description,
                    parent: data.parent,
                    child: [],
                    mart: "",
                    tabName: "test",
                    assetDs: "",
                    status: "pending"
                },
                relationships: {
                    job: {
                        data: {
                            type: "jobs",
                            // @ts-ignore
                            id: job.data.id
                        }
                    }
                }
            }
        }, event))
        // @ts-ignore
        const ds = JSON.parse(String(dsRes.output[1]))

        return ds.data
    }

    private async updateDfs(assetId: string, schemaJob: any, pyJob: any, event: Map<string, any>) {
        // 更新 Asset dfs关联关系
        await super.exec(this.genEvent(`PATCH`, `assets`, `/${assetId}?filter[isNewVersion]=true`, {
            data: {
                type: "assets",
                id: assetId,
                relationships: {
                    dfs: {
                        data: [
                            {
                                type: "data-sets",
                                id: schemaJob.id
                            },
                            {
                                type: "data-sets",
                                id: pyJob.id
                            }
                        ]
                    }
                }
            }
        }, event))
    }

    private async createDataMart(data: any, event: Map<string, any>) {
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const martName = dobj.martName
        const martUrl = dobj.martUrl
        const martDataType = dobj.martDataType
        const assetDescription = dobj.assetDescription
        const assetVersion = dobj.assetVersion
        const assetDataType = dobj.assetDataType
        const providers = [dobj.providers]
        const markets = [dobj.markets]
        const molecules = [dobj.molecules]
        const dataCover = [dobj.dataCover]
        const geoCover = [dobj.geoCover]
        const labels = [dobj.labels]
        const dfs = dobj.dfs.map((item) => {
            return {type: "data-sets", id: item}
        })

        const martRes = await super.exec(this.genEvent(`POST`, `marts`, ``, {
            data: {
                type: "marts",
                attributes: {
                    name: martName,
                    url: martUrl,
                    dataType: martDataType
                },
                relationships: {
                    dfs: { data: dfs }
                }
            }
        }, event))
        // @ts-ignore
        const mart = JSON.parse(martRes.output[1])

        await super.exec(this.genEvent(`POST`, `assets`, ``, {
            data: {
                type: "assets",
                attributes: {
                    name: dobj.assetName,
                    description: assetDescription,
                    version: assetVersion,
                    dataType: assetDataType,
                    providers,
                    markets,
                    molecules,
                    dataCover,
                    geoCover,
                    labels,
                    accessibility: `w`,
                    isNewVersion: true,
                    createTime: new Date()
                },
                relationships: {
                    mart: {
                        data: {
                            type: "marts",
                            id: mart.data.id
                        }
                    }
                }
            }
        }, event))
    }

    private async createDs(data: any, event: Map<string, any>, job: any) {
        const dobj = typeof data === "string" ? JSON.parse(data) : data
        const jobId = dobj.jobId
        const mongoId = dobj.mongoId
        const colNames = dobj.columnNames
        const parent = dobj.parentIds
        const length = dobj.length
        const tabName = dobj.tabName
        const description = dobj.description
        const url = dobj.url
        const body = {
            data: {
                type: "data-sets",
                attributes: { id: mongoId, parent, colNames, length, tabName, url, description }
            }
        }
        if (job !== null) {
            // @ts-ignore
            body.relationships = {
                job: {
                    data: {
                        type: "jobs",
                        id: job.data.id
                    }
                }
            }
        } else {
            const jobRes = await super.exec(this.genEvent(`POST`, `jobs`, ``, {
                data: {
                    type: "jobs",
                    attributes: {
                        jobContainerId: jobId,
                        create: new Date()
                    }
                }
            }, event))
            // @ts-ignore
            body.data.relationships = {
                job: {
                    data: {
                        type: "jobs",
                        // @ts-ignore
                        id: JSON.parse(String(jobRes.output[1])).data.id
                    }
                }
            }
        }
        await super.exec(this.genEvent(`POST`, `data-sets`, ``, body, event))
    }
}
