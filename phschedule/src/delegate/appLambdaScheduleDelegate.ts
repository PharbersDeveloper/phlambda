import * as fs from "fs"
import {JsonConvert} from "json2typescript"
import { v4 as uuidv4 } from "uuid"
import phLogger from "../logger/phLogger"
import {OssTask} from "../models/ossTask"
import AppLambdaDelegate from "./appLambdaDelegate"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */

// TODO: 先将原来的代码翻译过来
export default class AppLambdaScheduleDelegate extends AppLambdaDelegate {

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
                    break
                case "SandBoxDataSet":
                    break
                default:
                    phLogger.info("is not implementation")
                    break
            }
        }

        return null
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

        // TODO: Kafka Proxy topic oss_task_submit

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
        if (nextJob  && nextJob.next !== null ) {
            const dsRes = await super.exec(this.genEvent(`GET`, `data-sets`, `/${dsId}/child`, "", event))
            // @ts-ignore
            const ds = JSON.parse(String(dsRes.output[1]))
            const filterJob = ds.data.find((item) => item.attributes.description === nextJob.next)
            const nextJobRes = await super.exec(this.genEvent(`GET`, `jobs`, `/${filterJob.relationships.job.data.id}`, "", event))
            // @ts-ignore
            const next = JSON.parse(String(nextJobRes.output[1]))
            const nextJobId = next.data.attributes["job-container-id"]
            phLogger.info(nextJobId)
            // TODO 发送下一个Job开始 参数 nextJobId topic oss_msg
        } else {
            return null
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
}
