"use strict"
import AWS = require("aws-sdk")
import * as fs from "fs"
import { JsonConvert, OperationMode, ValueCheckingMode } from "json2typescript"
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
        const participants = []
        {
            PhLogger.info(`1. read Participant data in the excel`)

            const partData = XLSX.utils.sheet_to_json(wb.Sheets.Participant, { header: 2, defval: "" })
            const partResults = await Promise.all(partData.map( async (record: object) => {
                PhLogger.info("insert Participant one")
                // @ts-ignore
                const tmp = record.id
                // @ts-ignore
                delete record.id
                // @ts-ignore
                PhLogger.info(record.avatar)
                // @ts-ignore
                const m = imagesResults.filter((x) => x.id === parseInt(record.avatar, 10))
                // @ts-ignore
                record.avatar = m.map((x) => x.dbid)
                // if (m) {
                    // @ts-ignore
                    // record.avatar = m.dbid
                // }

                // @ts-ignore
                // record.host = []
                // @ts-ignore
                // record.speak = []
                // @ts-ignore
                // record.writeReports = []
                // @ts-ignore
                // PhLogger.info(record.avatar)
                // @ts-ignore
                const isr = await store.create("participant", record)
                return { id: tmp, dbid: isr.payload.records[0].id }
            }))
            // const jsonConvert: JsonConvert = new JsonConvert()
            // const th = new Participant()
            // participants = await Promise.all(data.map ( (x: any) => {
            //     jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
            //     jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
            //     jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
            //     const tmp = jsonConvert.deserializeObject(x, Participant)
            //     const avatarRef = images.find((it, indexA) =>  indexA.toString() === x.avatar.toString() )
            //     tmp.avatar = avatarRef
            //     return th.getModel().create(tmp)
            // }))
        }

        /**
         * 2. read events data in the excel
         * and colleect all the insertion ids
         */
        // let events: Event[] = []
        // {
        //     PhLogger.info(`2. read event data in the excel`)
        //
        //     const data = XLSX.utils.sheet_to_json(wb.Sheets.Event, { header: 2, defval: "" })
        //
        //     const jsonConvert: JsonConvert = new JsonConvert()
        //     const th = new Event()
        //     events = await Promise.all(data.map ( async (x: any) => {
        //         jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
        //         jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
        //         const tmp = jsonConvert.deserializeObject(x, Event)
        //         const eventSpeakers = x.speakers.toString().split("\n")
        //         const speakers = participants.filter((it, curIndex) => {
        //             const i = curIndex.toString()
        //             return eventSpeakers.includes(i)
        //         })
        //         tmp.speakers = speakers
        //         return th.getModel().create(tmp)
        //     }))
        // }

        /**
         * 3. read zone in the excel
         * and colleect all the insertion ids
         */
        // let zones: Zone[] = []
        // {
        //     PhLogger.info(`3. read zones in the excel`)
        //
        //     const data = XLSX.utils.sheet_to_json(wb.Sheets.Zone, { header: 2, defval: "" })
        //
        //     const jsonConvert: JsonConvert = new JsonConvert()
        //     const th = new Zone()
        //     zones = await Promise.all(data.map ( async (x: any) => {
        //         jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
        //         jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
        //         const tmp = jsonConvert.deserializeObject(x, Zone)
        //         const zoneHosts = x.hosts.toString().split("\n")
        //         const zoneAgendas = x.agendas.toString().split("\n")
        //         const hosts = participants.filter((it, curIndex) => {
        //             const i = curIndex.toString()
        //             return zoneHosts.includes(i)
        //         })
        //         const agendas = events.filter( (it, curIndex) => {
        //             const i = curIndex.toString()
        //             return zoneAgendas.includes(i)
        //         })
        //         tmp.hosts = hosts
        //         tmp.agendas = agendas
        //         tmp.avatar = await this.pushAvatar2Oss(tmp.avatarPath)
                // return th.getModel().create(tmp)
            // }))
        // }

        /**
         * 4. read requirement data in the excel
         * and colleect all the insertion ids
         */
        // let reports: Report[] = []
        // {
        //     PhLogger.info(`4. read Report data in the excel`)
        //
        //     const data = XLSX.utils.sheet_to_json(wb.Sheets.Report, { header: 2, defval: "" })
        //
        //     const jsonConvert: JsonConvert = new JsonConvert()
        //     const th = new Report()
        //     reports = await Promise.all(data.map ( (x: any) => {
        //         jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
                // jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                // jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                // const tmp = jsonConvert.deserializeObject(x, Report)
                // const coverRef = images.find((it, curIndex) => curIndex.toString() === x.cover.toString())
                // const reportWriter = x.writers
                // const writer = participants.filter((it, curIndex) => {
                //     const i = curIndex.toString()
                //     return reportWriter.includes(i)
                // })
                // tmp.writers = writer
                // tmp.cover = coverRef
                //
                // return th.getModel().create(tmp)
            // }))
        // }

        /**
         * 5. read cooperations data in the excel
         * and colleect all the insertion ids
         */
        // let cooperations: Cooperation[] = []
        // {
        //     PhLogger.info(`5. read Cooperations data in the excel`)
        //
        //     const data = XLSX.utils.sheet_to_json(wb.Sheets.Cooperation, { header: 2, defval: "" })
        //
        //     const jsonConvert: JsonConvert = new JsonConvert()
        //     const th = new Cooperation()
        //     cooperations = await Promise.all(data.map ( (x: any) => {
        //         jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
                // jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                // jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                // const tmp = jsonConvert.deserializeObject(x, Cooperation)
                // const logoRef = images.find((it, curIndex) => curIndex.toString() === x.logo.toString())
                // tmp.logo = logoRef
                // return th.getModel().create(tmp)
            // }))
        // }

        /**
         * 6. read hospital data in the excel
         * and collect all the insertion ids
         */
        // let activities: Activity[] = []
        // {
        //     PhLogger.info(`6. read acticity data in the excel`)
        //
        //     header:2 ?
            // const data = XLSX.utils.sheet_to_json(wb.Sheets.Activity, { header: 2, defval: "" })
            // const jsonConvert: JsonConvert = new JsonConvert()
            // const th = new Activity()
            //
            // activities = await Promise.all(data.map (async (x: any) => {
            //     jsonConvert.ignorePrimitiveChecks = true
            //     jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL
            //     const tmp = jsonConvert.deserializeObject(x, Activity)
            //     logo,logoOnTime,gallery 图片问题
                // const logoRef = images.find((it, curIndex) => curIndex.toString() === x.logo.toString())
                // const logoOnTimeRef = images.find((it, curIndex) => curIndex.toString() === x.logoOnTime.toString())
                // const acticityGallery = x.gallery.toString().split("\n")
                // const activityAttachment = x.attachments.toString().split("\n")
                // const activityAgenda = x.agendas.toString().split("\n")
                // const activityPartners = x.partners.toString().split("\n")
                // const attachments = reports.filter((it, curIndex) => {
                //     const i = curIndex.toString()
                //     return activityAttachment.includes(i)
                // })
                // const agendas = zones.filter((it, curIndex) => {
                //     const i = curIndex.toString()
                //     return activityAgenda.includes(i)
                // })
                // const galleryRef = images.filter((it, curIndex) => {
                //     const i = curIndex.toString()
                //     return acticityGallery.includes(i)
                // })
                // const partnersRef = cooperations.filter((it, curIndex) => {
                //     const i = curIndex.toString()
                //     return activityPartners.includes(i)
                // })
                // tmp.attachments = attachments
                // tmp.agendas = agendas
                // tmp.logo = logoRef
                // tmp.logoOnTime = logoOnTimeRef
                // tmp.gallery = galleryRef
                // tmp.partners = partnersRef
                // tmp.avatar = await this.pushAvatar2Oss(tmp.avatarPath)
                // return th.getModel().create(tmp)
            // }))
        // }
    }
}
