"use strict"
import AWS = require("aws-sdk")
import * as fs from "fs"
import * as path from "path"
import XLSX = require("xlsx")
import PhLogger from "../logger/phLogger"

export default class ExcelDataInputOffweb {

    public excelPath?: string
    public assetsPath?: string

    constructor(event: object) {
        // @ts-ignore
        this.excelPath = event.excelPath
        // @ts-ignore
        this.assetsPath = event.assetsPath
    }

    public async excelModelData(store: object) {
        PhLogger.info(`start input data with excel`)
        const file = this.excelPath
        return await this.loadExcelData(file, store) // 将数据导入到数据库
        // await this.uploadAssets() // 将文件上传到s3
    }

    public async uploadAssets() {
        // 0. init oss
        // Set the Region
        AWS.config.update({region: "cn-northwest-1"})
        const s3 = new AWS.S3({apiVersion: "2006-03-01"})

        // 1. create bucket
        // const bucketParams = {
        //     Bucket: "ph-offweb",
        //     ACL: "public-read"
        // }

        // s3.createBucket(bucketParams, function(err:any, data:any) {
        //     if (err) {
        //        PhLogger.info("Error", err);
        //       } else {
        //        PhLogger.info("Success", data.Location);
        //       }
        // })

        // 需要改成参数传入/配置 >>> assetsPath
        // const assetsDir = "test/data/offweb/assets"
        const assetsDir = this.assetsPath
        const that = this
        const arr: any = []

        // 遍历文件夹
        this.readFileList(assetsDir, arr)

        for (const item of arr) {
            const s3key =  "public/" + that.getFileName(item)
            const existsQuery = {
                Bucket: "ph-offweb",
                Key: s3key,
                Range: "bytes=0-9"
            }
            await s3.getObject(existsQuery).promise().catch(async (reason: any) => {
                if (reason.code === "NoSuchKey") {
                    /**
                     * 优先上传文件, 到S3
                     */
                    const uploadParams = {Bucket: "ph-offweb", Key: s3key, Body: "", ContentType: ""}
                    const fileKeyName = item
                    const nameArr = item.split(".")
                    const imageType = nameArr[1]

                    if (imageType === "svg") {
                        uploadParams.ContentType = "image/svg+xml"
                    } else if (imageType === "png") {
                        uploadParams.ContentType = "image/png"
                    } else if (imageType === "jpg" || imageType === "jpeg") {
                        uploadParams.ContentType = "image/jpeg"
                    }
                    // Configure the file stream and obtain the upload parameters
                    // @ts-ignore
                    uploadParams.Body = await fs.createReadStream(fileKeyName)
                    // uploadParams.Body = await fs.createReadStream("/Users/alfredyang/Desktop/upload.xlsx")
                    // call S3 to retrieve upload file to specified bucket
                    return s3.upload(uploadParams).promise()
                }
            })
        }
    }

    public readFileList(assetsDir: any, filesList: any) {
        const that = this
        const files = fs.readdirSync(assetsDir)
        files.forEach((itm) => {
            const filePath = path.join(assetsDir, itm)
            const stat = fs.statSync(filePath)
            if (stat.isDirectory()) {
                that.readFileList(filePath, filesList)
            } else {
                filesList.push(filePath)
            }
        })
    }

    public getFileName(fpath: string) {
        if (fpath.indexOf("/") >= 0) {
            return fpath.substr(fpath.lastIndexOf("/") + 1)
        } else {
            return fpath.substr(fpath.lastIndexOf("\\") + 1)
        }
    }

    public async loadExcelData(file: string, store: object) {
        const wb = XLSX.readFile(file)

        /**
         * 0. read Image data in the excel
         * and colleect all the insertion ids
         */
        PhLogger.info(`0. read Image data in the excel`)

        const imageData = XLSX.utils.sheet_to_json(wb.Sheets.Image, { header: 2, defval: "" })
        const imagesResults = await Promise.all(imageData.map( async (record: object) => {
            PhLogger.info("insert Image one")
            // @ts-ignore
            const tmp: string = record.id as string
            // @ts-ignore
            delete record.id
            // @ts-ignore
            const isr = await store.create("image", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 1. read Participant data in the excel
         * and colleect all the insertion ids
         */
        PhLogger.info(`1. read Participant data in the excel`)

        const partData = XLSX.utils.sheet_to_json(wb.Sheets.Participant, { header: 2, defval: "" })
        const partResults = await Promise.all(partData.map( async (record: object) => {
            PhLogger.info("insert Participant one")
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id
            // @ts-ignore
            const m = imagesResults.find((x) => x.id === parseInt(record.avatar, 10))
            if (m) {
                // @ts-ignore
                record.avatar = m.dbid
            } else {
                // @ts-ignore
                record.avatar = null
            }

            // @ts-ignore
            const isr = await store.create("participant", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 2. read events data in the excel
         * and colleect all the insertion ids
         */
        PhLogger.info(`2. read event data in the excel`)

        const eventData = XLSX.utils.sheet_to_json(wb.Sheets.Event, { header: 2, defval: "" })

        const eventResult = await Promise.all(eventData.map( async (record: object) => {
            PhLogger.info("insert event one")
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id

            // @ts-ignore
            const eventSpeakers = record.speakers.toString().split("\n")
            // @ts-ignore
            record.speakers = eventSpeakers.map((s) => {
                const m = partResults.find((x) => x.id === parseInt(s, 10))
                if (m) {
                    return m.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            if (record.startDate === "") {
                // @ts-ignore
                delete record.startDate
                // record.startDate = new Date()
            } else {
                // @ts-ignore
                record.startDate = new Date(parseInt(record.startDate, 10))
            }

            // @ts-ignore
            if (record.endDate === "") {
                // @ts-ignore
                delete record.endDate
                // record.endDate = new Date()
            } else {
                // @ts-ignore
                record.endDate = new Date(parseInt(record.endDate, 10))
            }

            // @ts-ignore
            const isr = await store.create("event", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 3. read zone in the excel
         * and colleect all the insertion ids
         */
        PhLogger.info(`3. read zones in the excel`)

        const zoneData = XLSX.utils.sheet_to_json(wb.Sheets.Zone, { header: 2, defval: "" })
        const zoneResult = await Promise.all(zoneData.map(async (record: object) => {
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id

            // @ts-ignore
            const tmpHosts = record.hosts.toString().split("\n")
            // @ts-ignore
            record.hosts = tmpHosts.map((s) => {
                const m = partResults.find((x) => x.id === parseInt(s, 10))
                if (m) {
                    return m.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const tmpAgendas = record.agendas.toString().split("\n")
            // @ts-ignore
            record.agendas = tmpAgendas.map((s) => {
                const m = eventResult.find((x) => x.id === parseInt(s, 10))
                if (m) {
                    return m.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            if (record.startDate === "") {
                // @ts-ignore
                delete record.startDate
                // record.startDate = new Date()
            } else {
                // @ts-ignore
                record.startDate = new Date(parseInt(record.startDate, 10))
            }

            // @ts-ignore
            if (record.endDate === "") {
                // @ts-ignore
                delete record.endDate
                // record.endDate = new Date()
            } else {
                // @ts-ignore
                record.endDate = new Date(parseInt(record.endDate, 10))
            }

            // @ts-ignore
            const isr = await store.create("zone", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 4. read requirement data in the excel
         * and colleect all the insertion ids
         */
        // let reports: Report[] = []
        // {
        PhLogger.info(`4. read Report data in the excel`)

        const reportDate = XLSX.utils.sheet_to_json(wb.Sheets.Report, { header: 2, defval: "" })
        const reportResult = await Promise.all(reportDate.map(async (record: object) => {
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id

            // @ts-ignore
            const m = imagesResults.find((x) => x.id === parseInt(record.cover, 10))
            if (m) {
                // @ts-ignore
                record.cover = m.dbid
            } else {
                // @ts-ignore
                record.cover = null
            }

            // @ts-ignore
            if (record.date === "") {
                // @ts-ignore
                delete record.date
                // record.endDate = new Date()
            } else {
                // @ts-ignore
                record.date = new Date(parseInt(record.date, 10))
            }

            // @ts-ignore
            const tmpWriter = record.writers.toString().split("\n")
            // @ts-ignore
            record.writers = tmpWriter.map((s) => {
                const t = partResults.find((x) => x.id === parseInt(s, 10))
                if (t) {
                    return t.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const isr = await store.create("report", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 5. read cooperations data in the excel
         * and colleect all the insertion ids
         */
        PhLogger.info(`5. read Cooperations data in the excel`)

        const corData = XLSX.utils.sheet_to_json(wb.Sheets.Cooperation, { header: 2, defval: "" })
        const corResult = await Promise.all(corData.map(async (record: object) => {
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id

            // @ts-ignore
            const m = imagesResults.find((x) => x.id === parseInt(record.logo, 10))
            if (m) {
                // @ts-ignore
                record.logo = m.dbid
            } else {
                // @ts-ignore
                record.logo = null
            }

            // @ts-ignore
            const isr = await store.create("cooperation", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))

        /**
         * 6. read hospital data in the excel
         * and collect all the insertion ids
         */
        PhLogger.info(`6. read acticity data in the excel`)

        const actData = XLSX.utils.sheet_to_json(wb.Sheets.Activity, { header: 2, defval: "" })
        const actResult = await Promise.all(actData.map(async (record: object) => {
            // @ts-ignore
            const tmp = record.id
            // @ts-ignore
            delete record.id

            // @ts-ignore
            if (record.startDate === "") {
                // @ts-ignore
                delete record.startDate
                // record.startDate = new Date()
            } else {
                // @ts-ignore
                record.startDate = new Date(parseInt(record.startDate, 10))
            }

            // @ts-ignore
            if (record.endDate === "") {
                // @ts-ignore
                delete record.endDate
                // record.endDate = new Date()
            } else {
                // @ts-ignore
                record.endDate = new Date(parseInt(record.endDate, 10))
            }

            // @ts-ignore
            const m = imagesResults.find((x) => x.id === parseInt(record.logo, 10))
            if (m) {
                // @ts-ignore
                record.logo = m.dbid
            } else {
                // @ts-ignore
                record.logo = null
            }

            // @ts-ignore
            const lm = imagesResults.find((x) => x.id === parseInt(record.logoOnTime, 10))
            if (lm) {
                // @ts-ignore
                record.logoOnTime = lm.dbid
            } else {
                // @ts-ignore
                record.logoOnTime = null
            }

            // @ts-ignore
            const gx = record.gallery.toString().split("\n")
            // @ts-ignore
            record.gallery = gx.map((s) => {
                // @ts-ignore
                const g = imagesResults.find((x) => x.id === parseInt(s, 10))
                if (g) {
                    return g.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const at = record.attachments.toString().split("\n")
            // @ts-ignore
            record.attachments = at.map((s) => {
                // @ts-ignore
                const a = reportResult.find((x) => x.id === parseInt(s, 10))
                if (a) {
                    return a.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const ad = record.agendas.toString().split("\n")
            // @ts-ignore
            record.agendas = ad.map((s) => {
                // @ts-ignore
                const d = zoneResult.find((x) => x.id === parseInt(s, 10))
                if (d) {
                    return d.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const pt = record.partners.toString().split("\n")
            // @ts-ignore
            record.partners = pt.map((s) => {
                // @ts-ignore
                const p = corResult.find((x) => x.id === parseInt(s, 10))
                if (p) {
                    return p.dbid
                } else {
                    return undefined
                }
            }).filter((x) => x !== undefined)

            // @ts-ignore
            const isr = await store.create("activity", record)
            return { id: tmp, dbid: isr.payload.records[0].id }
        }))
        PhLogger.info(actResult)
    }
}
