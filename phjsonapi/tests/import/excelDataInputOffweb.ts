import AWS = require("aws-sdk")
import * as fs from "fs"
import { JsonConvert, OperationMode, ValueCheckingMode } from "json2typescript"
import { slow, suite, test, timeout } from "mocha-typescript"
import mongoose = require("mongoose")
import * as path from "path"
// import uuidv4 from "uuid/v4"
import XLSX = require("xlsx")
import PhLogger from "../../src/logger/phLogger"
import Activity from "../../src/models/offweb/activity"
import Cooperation from "../../src/models/offweb/cooperation"
import Event from "../../src/models/offweb/event"
import Participant from "../../src/models/offweb/participant"
import Report from "../../src/models/offweb/report"
import Zone from "../../src/models/offweb/zone"
// import e = require("express")

@suite(timeout(1000 * 60), slow(2000))
class ExcelDataInputOffweb {

    public static before() {
        PhLogger.info(`before starting the test`)
        mongoose.connect("mongodb://pharbers.com:5555/pharbers-offweb")
        // mongoose.connect("mongodb://localhost:27017/pharbers-ntm-client")
    }

    public static after() {
        PhLogger.info(`after starting the test`)
        mongoose.disconnect()
    }

    // constructor() {
    // }

    @test public async excelModelData() {
        PhLogger.info(`start input data with excel`)
        const file = "test/data/offweb/offweb.xlsx"

        await this.loadExcelData(file)
        await this.uploadAssets()
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
        //         PhLogger.info("Error", err);
        //       } else {
        //         PhLogger.info("Success", data.Location);
        //       }
        // })

        // 需要改成参数传入/配置
        const assetsDir = "test/data/offweb/assets"
        const that = this
        const arr: any = []

        // 遍历文件夹
        this.readFileList(assetsDir, arr)

        arr.forEach(async (item: any) => {
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
                    const uploadParams = {Bucket: "ph-offweb", Key: s3key, Body: ""}
                    const fileKeyName = item

                    // Configure the file stream and obtain the upload parameters
                    // @ts-ignore
                    uploadParams.Body = await fs.createReadStream(fileKeyName)
                    // uploadParams.Body = await fs.createReadStream("/Users/alfredyang/Desktop/upload.xlsx")
                    // call S3 to retrieve upload file to specified bucket
                    s3.upload(uploadParams).promise()
                }
            })
        })
    }

    // 异步读文件，暂时无用
    // public async getFiles(assetsDir: any, fileArr: any, callback?:any ) {
    //     let that = this
    //     fs.readdir(assetsDir, function(err, files) {
    //         if (err) {
    //             throw err
    //         }
    //         files.forEach(file => {
    //             let filePath = path.join(assetsDir, file);
    //             fs.stat(filePath, function(err, stat) {
    //                 if (stat.isFile()) {
    //                     fileArr.push(filePath)
    //                 } else {
    //                     files.push()
    //                     that.getFiles(filePath, fileArr )
    //                 }
    //             })
    //         })
    //     })
    //     callback && callback.call()
    // }

    public readFileList(assetsDir: any, filesList: any) {
        const that = this
        const files = fs.readdirSync(assetsDir)
        files.forEach((itm, index) => {
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

    public async loadExcelData(file: string) {
        const wb = XLSX.readFile(file)

        /**
         * 1. read Participant data in the excel
         * and colleect all the insertion ids
         */
        let participants: Participant[] = []
        {
            PhLogger.info(`1. read Participant data in the excel`)

            const data = XLSX.utils.sheet_to_json(wb.Sheets.Participant, { header: 2, defval: "" })

            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Participant()
            participants = await Promise.all(data.map ( (x: any) => {
                // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
                jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                return th.getModel().create(jsonConvert.deserializeObject(x, Participant))
            }))
        }

        /**
         * 2. read events data in the excel
         * and colleect all the insertion ids
         */
        let events: Event[] = []
        {
            PhLogger.info(`2. read event data in the excel`)

            const data = XLSX.utils.sheet_to_json(wb.Sheets.Event, { header: 2, defval: "" })

            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Event()
            events = await Promise.all(data.map ( async (x: any) => {
                jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                const tmp = jsonConvert.deserializeObject(x, Event)
                const eventSpeakers = x.speakers.toString().split("\n")
                const speakers = participants.filter((it, index) => {
                    const i = index.toString()
                    return eventSpeakers.includes(i)
                })
                tmp.speakers = speakers
                return th.getModel().create(tmp)
            }))
        }

        /**
         * 3. read zone in the excel
         * and colleect all the insertion ids
         */
        let zones: Zone[] = []
        {
            PhLogger.info(`3. read zones in the excel`)

            const data = XLSX.utils.sheet_to_json(wb.Sheets.Zone, { header: 2, defval: "" })

            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Zone()
            zones = await Promise.all(data.map ( async (x: any) => {
                jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                const tmp = jsonConvert.deserializeObject(x, Zone)
                const zoneHosts = x.hosts.toString().split("\n")
                const zoneAgendas = x.agendas.toString().split("\n")
                const hosts = participants.filter((it, index) => {
                    const i = index.toString()
                    return zoneHosts.includes(i)
                })
                const agendas = zones.filter( (it, index) => {
                    const i = index.toString()
                    return zoneAgendas.includes(i)
                })
                tmp.hosts = hosts
                tmp.agendas = agendas
                // tmp.avatar = await this.pushAvatar2Oss(tmp.avatarPath)
                return th.getModel().create(tmp)
            }))
        }

        /**
         * 4. read requirement data in the excel
         * and colleect all the insertion ids
         */
        let reports: Report[] = []
        {
            PhLogger.info(`4. read Report data in the excel`)

            const data = XLSX.utils.sheet_to_json(wb.Sheets.Report, { header: 2, defval: "" })

            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Report()
            reports = await Promise.all(data.map ( (x: any) => {
                // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
                jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                const tmp = jsonConvert.deserializeObject(x, Report)
                const reportWriter = x.writers
                const writer = participants.filter((it, index) => {
                    const i = index.toString()
                    return reportWriter.includes(i)
                })
                tmp.writers = writer
                // 有个封面要上传
                return th.getModel().create(tmp)
            }))
        }

        /**
         * 5. read cooperations data in the excel
         * and colleect all the insertion ids
         */
        let cooperations: Cooperation[] = []
        {
            PhLogger.info(`5. read Cooperations data in the excel`)

            const data = XLSX.utils.sheet_to_json(wb.Sheets.Cooperation, { header: 2, defval: "" })

            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Cooperation()
            cooperations = await Promise.all(data.map ( (x: any) => {
                // jsonConvert.operationMode = OperationMode.LOGGING // print some debug data
                jsonConvert.ignorePrimitiveChecks = true // don't allow assigning number to string etc.
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL // never allow null
                const tmp = jsonConvert.deserializeObject(x, Cooperation)
                // 有个logo要上传的哈
                return th.getModel().create(tmp)
            }))
        }

        /**
         * 6. read hospital data in the excel
         * and collect all the insertion ids
         */
        let activities: Activity[] = []
        {
            PhLogger.info(`6. read acticity data in the excel`)

            // header:2 ?
            const data = XLSX.utils.sheet_to_json(wb.Sheets.Activity, { header: 2, defval: "" })
            const jsonConvert: JsonConvert = new JsonConvert()
            const th = new Activity()

            activities = await Promise.all(data.map (async (x: any) => {
                jsonConvert.ignorePrimitiveChecks = true
                jsonConvert.valueCheckingMode = ValueCheckingMode.DISALLOW_NULL
                const tmp = jsonConvert.deserializeObject(x, Activity)
                // logo,logoOnTime,gallery 图片问题
                const activityAttachment = x.attachments.toString().split("\n")
                const activityAgenda = x.agendas.toString().split("\n")
                const attachments = reports.filter((it, index) => {
                    const i = index.toString()
                    return activityAttachment.includes(i)
                })
                const agendas = zones.filter((it, index) => {
                    const i = index.toString()
                    return activityAgenda.includes(i)
                })
                tmp.attachments = attachments
                tmp.agendas = agendas
                // tmp.avatar = await this.pushAvatar2Oss(tmp.avatarPath)
                return th.getModel().create(tmp)
            }))
        }
    }
}
