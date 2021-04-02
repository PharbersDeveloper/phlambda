import AWS from "aws-sdk"
import S3 from "aws-sdk/clients/s3"
import fortune from "fortune"
import { SF, Store } from "phnodelayer"
import { ConfigRegistered, PostgresConfig } from "phnodelayer"
// @ts-ignore
import R from "ramda"
import uuidv4 from "uuid/v4"
import XLSX = require("xlsx")

// @ts-ignore
export async function exportsHandler(event: Map<string, any>) {
    // const localPath: string = process.env.PH_TS_SERVER_HOME + "/tmp/"
    const localPath: string = "/tmp/"
    const exportDir: string = "tm-export/"
    const suffix: string = ".xlsx"
    // @ts-ignore
    const body = JSON.parse(event.body).data.attributes
    console.log(body)
    const projectId = body.projectId
    const phase = body.phase
    const uid = body.uid
    let isReport = body.isReport
    console.log(projectId, phase, uid, isReport)
    const postgres = SF.getInstance.get(Store.Postgres)
    await postgres.open()
    // console.log("curProject result")
    // const curProject = await postgres.find("project", null, { match: { projectId } }) rR9lwp8e55q9izZdHdQZ
    function formatPhaseToStringDefault( date: any ) {
        const year = date.getFullYear()
        const month = date.getMonth()
        let season = ""

        switch ( true ) {
            case month < 3:
                season = "Q1"
                break
            case month < 6:
                season = "Q2"
                break
            case month < 9:
                season = "Q3"
                break
            default:
                season = "Q4"
                break
        }
        return `${year}${season}`
    }
    // tslint:disable-next-line:no-shadowed-variable
    function formatPhaseToDate( OriginBasePhase: any, step: any, phase: any ) {

        const basePhase = new Date( OriginBasePhase )
        const year = basePhase.getFullYear()
        const month = basePhase.getMonth()
        const date = basePhase.getDate()
        let newYear = year
        let newMonth = month
        let newDate = date
        const unit = step.slice( -1 )
        const stepNum = parseInt( step, 10 )

        if ( ["y", "Y"].includes( unit ) ) {
            newYear = year + stepNum * phase
            basePhase.setFullYear( newYear )
        } else if ( ["m", "M"].includes( unit ) ) {
            newMonth = month + stepNum * phase
            basePhase.setMonth( newMonth )
        } else if ( ["w", "W"].includes( unit ) ) {
            newDate = date + stepNum * 7 * phase
            basePhase.setFullYear( newYear )
        } else if ( ["d", "D"].includes( unit ) ) {
            newDate = date + stepNum * phase
            basePhase.setDate( newDate )
        }

        return basePhase
    }
    /**
     * 1.找到当前project下的周期
     */
    const curProjectObject = await postgres.find("project", "rR9lwp8e55q9izZdHdQZ")
    const curProject = JSON.parse(JSON.stringify(curProjectObject.payload.records))[0]
    // console.log(curProject)
    const currentPhase = parseInt(phase, 10)
    /**
     * 2.获取当前proposal
     */
    const proposalId = curProject.proposal
    const curProposalObject = await postgres.find("proposal", proposalId)
    const curProposal = JSON.parse(JSON.stringify(curProposalObject.payload.records))[0]
    // console.log(curProposal)
    /**
     * 3.获取当前的proposal下所有参与的hospital
     */
    const hospIds = curProposal.targets
    const hospitalsObject = await postgres.find("hospital", hospIds)
    const hospitals = JSON.parse(JSON.stringify(hospitalsObject.payload.records))
    // console.log(hospitals)
    /**
     * 4.获取当前的proposal下所有参与的products
     */
    const prodIds = curProposal.products
    const productsObject = await postgres.find("product", prodIds)
    const products = JSON.parse(JSON.stringify(productsObject.payload.records))
    // console.log(products)
    /**
     * 5.获取当前的proposal下所有参与的resources
     */
    const resIds = curProposal.products
    const resourcesObject = await postgres.find("product", prodIds)
    const resources = JSON.parse(JSON.stringify(resourcesObject.payload.records))
    // console.log(resources)
    let unSortData: any[] = []
    let headers: Array<Array<string | number>> = []
    // const proposalCase = curProposal.case
    const proposalCase = "tm"
    isReport = false
    if (isReport) {
        // @ts-ignore
        if (proposalCase === "ucb") {
            headers = [
                ["周期", "城市名称", "医院名称", "医院等级", "负责代表", "产品", "进药状态", "患者数量", "指标达成率", "销售额"]
            ]
        } else if (proposalCase === "tm") {
            headers = [
                ["周期", "城市名称", "医院名称", "医院等级", "负责代表", "产品", "潜力", "指标达成率", "销售额"]
            ]
        }
        /**
         * 6. 从数据库中拉取数据Report
         */
        // tslint:disable-next-line:max-line-length
        const reportsObject = await postgres.find("report", null, { or: { projectId, proposalId: proposalId.toString()}, match: {category: "Hospital"}, range: {phase: [0, currentPhase]}, sort: {phase: true}})
        const reports = JSON.parse(JSON.stringify(reportsObject.payload.records))
        // tslint:disable-next-line:max-line-length
        const presetsObject = await postgres.find("preset", null, { or: { projectId, proposalId: proposalId.toString()}, match: {category: 8}, range: {phase: [0, currentPhase]}})
        const presets = JSON.parse(JSON.stringify(presetsObject.payload.records))
        unSortData = reports.map( (x, index) => {
            const hospital = hospitals.find((h) => h.id === x.hospital.toString())
            const tmprid = x.resource ? x.resource.toString() : ""
            const resource = resources.find((r) => r.id === tmprid)
            const product = products.find((p) => p.id === x.product.toString())

            const condi = (pp) => {
                if (x.phase < 0) {
                    return pp.phase - 1 === x.phase &&
                        pp.projectId === "" &&
                        pp.hospital.toString() === x.hospital.toString() &&
                        pp.product.toString() === x.product.toString()
                } else {
                    return pp.phase - 1 === x.phase &&
                        pp.projectId === projectId &&
                        pp.hospital.toString() === x.hospital.toString() &&
                        pp.product.toString() === x.product.toString()
                }
            }

            const cpp = presets.find(condi)

            let entrance = ""
            if (cpp) {
                if (cpp.currentDurgEntrance === "1") {
                    entrance = "已开发"
                } else if (cpp.currentDurgEntrance === "2") {
                    entrance = "正在开发"
                } else {
                    entrance = "未开发"
                }
            }

            let pss = ""
            pss = formatPhaseToStringDefault(
                formatPhaseToDate( curProposal.periodBase, curProposal.periodStep, x.phase )
            )
            // console.log(pss)

            switch (x.phase) {
                case -4:
                    pss = "2018Q1"
                    break
                case -3:
                    pss = "2018Q2"
                    break
                case -2:
                    pss = "2018Q3"
                    break
                case -1:
                    pss = "2018Q4"
                    break
                // case 0:
                //     pss = "2019Q1"
                //     break
                // case 1:
                //     pss = "2019Q2"
                //     break
                // case 2:
                //     pss = "2019Q3"
                //     break
                default:
                // pss = ""
            }
            const qFunc = (qa: number, q: number) => {
                if (qa > 0) {
                    return qa.toFixed(3)
                } else if ( q === 0) {
                    return 0
                } else {
                    return 0
                }
            }

            const achiTMFunc = (sales: number, salesQuota: number) => {
                if (salesQuota === 0) {
                    return 0
                } else {
                    return (sales / salesQuota).toFixed(3)
                }
            }

            let potentialOrPatient = 0
            let achi = null
            // @ts-ignore
            if (proposalCase === "ucb") {
                const a = x.phase < 0 ? x.achievements : cpp.lastAchievement
                const b = x.phase < 0 ? x.salesQuota : cpp.lastQuota

                potentialOrPatient = cpp ? cpp.currentPatientNum : 0
                achi = qFunc(a, b)
            } else if (proposalCase === "tm") {
                potentialOrPatient = cpp ? cpp.potential : 0
                achi = achiTMFunc(x.sales, x.salesQuota)
            }
            // @ts-ignore
            if (proposalCase === "ucb") {
                return [
                    pss, // 0
                    hospital.position,
                    hospital.name, // 2
                    hospital.level,
                    resource ? resource.name : "未分配",
                    product ? product.name : "",
                    entrance,
                    potentialOrPatient, // 7
                    // tm 潜力, ucb 病患数量
                    // tslint:disable-next-line: max-line-length
                    achi,
                    x.sales ? x.sales.toFixed(0) : 0 // 9
                ]
            } else if (proposalCase === "tm") {
                return [
                    pss, // 0
                    hospital.position,
                    hospital.name, // 2
                    hospital.level,
                    resource ? resource.name : "未分配",
                    product ? product.name : "",
                    potentialOrPatient, // 7
                    // tm 潜力, ucb 病患数量
                    // tslint:disable-next-line: max-line-length
                    achi,
                    x.sales ? x.sales.toFixed(0) : 0 // 9
                ]
            }
        })
    } else {
        headers = [
            ["周期", "代表", "医院", "产品名称", "销售指标分配", "预算分配"]
        ]
        /**
         * inputReport
         */
        const perIds = curProject.periods.map( (x) => {
            return x
        } )
        const allPeriodsObject = await postgres.find("period", null, { or: { perIds }})
        const allPeriods = JSON.parse(JSON.stringify(allPeriodsObject.payload.records))
        // tslint:disable-next-line:prefer-for-of
        for (let i = 0; i < allPeriods.length ; i++) {
            const phaseAnsIds = allPeriods[i].answers.map( (x) => {
                return x
            } )
            const phaseAnswersObject = await postgres.find("answer", null, { or: { phaseAnsIds }})
            const phaseAnswers = JSON.parse(JSON.stringify(phaseAnswersObject.payload.records))
            // console.log("phaseAnswers" + i)
            // console.log(phaseAnswers)
            const handledPhaseAnswers = phaseAnswers.map((ele, idx) => {
                const hospital = hospitals.find((h) => h.id === ele.target ? ele.target.toString() : "")
                const resource = resources.find((r) => r.id === ele.resource ? ele.resource.toString() : "")
                const product = products.find((p) => p.id === ele.product ? ele.product.toString() : "")
                return [
                    allPeriods[i].name,
                    resource ? resource.name : "未分配",
                    hospital ? hospital.name : "",
                    product ? product.name : "",
                    ele.salesTarget,
                    ele.budget
                ]
            })
            unSortData = unSortData.concat(handledPhaseAnswers)
            // console.log("unSortData" + i)
            // console.log(unSortData)
        }
    }

    // tm potential 2018Q1 2018Q2 2018Q3 <== 2018Q4
    if (proposalCase === "tm") {
        const Q4 = unSortData.filter((item) => item[0] === "2018Q4")
        const blankPotentialQ =
            unSortData.filter((item) => item[0] === "2018Q1" || item[0] === "2018Q2" || item[0] === "2018Q3")
        for (const row of Q4) {
            const rowHospital = row[2]
            const rowProduct = row[5]
            const rowPotential = row[6]

            const curRow =
                blankPotentialQ.filter((item) => item[2] === rowHospital && item[5] === rowProduct)

            for (const blankP of curRow) {
                blankP[6] = rowPotential
            }
        }

    }

    /**
     * 1. group by pss
     */
    const toPhase = ((x: Array<string | number>) => {
        return x[0] as string
    } )
    const grouped = R.groupBy(toPhase, unSortData)
    // console.log(grouped)
    let fr: Array<Array<string | number>> = []
    for (const key of Object.keys(grouped)) {
        const rd = grouped[key]

        /**
         * 2. to every phase, reduceBy hospital
         */
        const toHos = ((x: Array<string | number>) => {
            return x[2] as string
        } )

        const hos = R.groupBy(toHos, rd)

        const sortFunc =
            (left: Array<string | number>, right: Array<string | number>) => {
                const m = (right[7] as number) - (left[7] as number)
                return m === 0 ? (right[9] as number) - (left[9] as number) : m
            }

        const sortFuncTM =
            (left: Array<string | number>, right: Array<string | number>) => {
                const m = (right[6] as number) - (left[6] as number)
                return m === 0 ? (right[8] as number) - (left[8] as number) : m
            }

        const nhos = Object.keys(hos).map((x) => {
            // @ts-ignore
            if (proposalCase === "ucb") {
                const ht = hos[x].sort(sortFunc)
                return { key: x, lst: ht }
            } else if (proposalCase === "tm") {
                const ht = hos[x].sort(sortFuncTM)
                return { key: x, lst: ht }
            }
        } )

        const patNum = (acc: number, item: Array<string | number>) => acc += item[7] as number
        const potentialNum = (acc: number, item: Array<string | number>) => acc += item[6] as number
        // @ts-ignore
        const reduce = proposalCase === "ucb" ?
            R.reduceBy(patNum, 0, toHos, rd) : R.reduceBy(potentialNum, 0, toHos, rd)

        /**
         * 3. sort hospital in the phase
         */
        const sortArr = Object.keys(reduce).map((x: string) => {
            return { key: x, value: reduce[x] }
        })
        const sortedWithPat = R.sort((left, right) => right.value - left.value, sortArr)

        let result: Array<Array<string | number>> = []
        sortedWithPat.forEach( (item) => {
            result = result.concat(nhos.find((x) => x.key === item.key).lst)
        } )
        fr = fr.concat(result)
        // console.log(fr)
    }

    const data = headers.concat(fr)
    const jobId = uuidv4()
    const workbook = XLSX.utils.book_new() // 创建新的workbook
    const worksheet = XLSX.utils.aoa_to_sheet(data) // make a cd sheet
    // console.log(worksheet)
    workbook.Props = {
        Author: "Alfred Yang",
        CreatedDate: new Date(),
        Subject: "TM-Export",
        Title: jobId + suffix,
    }
    XLSX.utils.book_append_sheet(workbook, worksheet, "TM-Export") // append the sheet to the workbook
    XLSX.writeFile(workbook,  jobId + suffix)
    // // 获取数据
    // const excelBuffer = await XLSX.readFile(jobId + suffix)
    //
    // // 解析数据
    // const result = XLSX.read(excelBuffer, {
    //     type: "buffer",
    //     cellHTML: false,
    // })
    //
    // console.log("TCL: result", result)

    /**
     * aws s3 upload
     */
    const credentials = {
        accessKeyId: "AKIAWPBDTVEAPOX3QT6U",
        secretAccessKey: "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",
        region: "cn-northwest-1",
    }
    AWS.config.update( credentials )
    const s3 = new AWS.S3({apiVersion: "2006-03-01"})
    const bucketName = "ph-origin-files"
    // console.log(localPath + jobId + suffix)
    const fileKey = `export/${ uid }/${ jobId + suffix }`
    const uploadFileParams = {
        Bucket: bucketName,
        Key: fileKey,
        Body: Buffer.from(JSON.stringify(workbook), "binary")
    }
    const response = await s3.upload(uploadFileParams, ).promise()
    return {
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        status: 200,
        message: {
            message: "success",
            Location: response.Location,
            Bucket: response.Bucket,
            key: response.Key
        }
    }
}
