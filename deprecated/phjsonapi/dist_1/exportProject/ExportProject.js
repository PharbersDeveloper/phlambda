"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const ali_oss_1 = __importDefault(require("ali-oss"));
const ramda_1 = __importDefault(require("ramda"));
const v4_1 = __importDefault(require("uuid/v4"));
const XLSX = require("xlsx");
const phLogger_1 = __importDefault(require("../logger/phLogger"));
const phLogger_2 = __importDefault(require("../logger/phLogger"));
const Answer_1 = __importDefault(require("../models/ntm/Answer"));
const Hospital_1 = __importDefault(require("../models/ntm/Hospital"));
const Period_1 = __importDefault(require("../models/ntm/Period"));
const Preset_1 = __importDefault(require("../models/ntm/Preset"));
const Product_1 = __importDefault(require("../models/ntm/Product"));
const Project_1 = __importDefault(require("../models/ntm/Project"));
const Proposal_1 = __importDefault(require("../models/ntm/Proposal"));
const Report_1 = __importDefault(require("../models/ntm/Report"));
const Resource_1 = __importDefault(require("../models/ntm/Resource"));
class ExportProejct {
    constructor(oss) {
        this.client = null;
        this.localPath = process.env.PH_TS_SERVER_HOME + "/tmp/";
        this.exportDir = "tm-export/";
        this.suffix = ".xlsx";
        if (oss) {
            this.client = new ali_oss_1.default({
                accessKeyId: oss.accessKeyId,
                accessKeySecret: oss.accessKeySecret,
                bucket: oss.bucket,
                region: oss.region,
            });
        }
    }
    pushResult2OSS(jobId) {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.client) {
                try {
                    const r1 = yield this.client.put(this.exportDir + jobId + this.suffix, this.localPath + jobId + this.suffix);
                    phLogger_1.default.info("put success: %j", r1);
                    // let r2 = await this.client.get('object');
                    // console.log('get success: %j', r2);
                }
                catch (err) {
                    phLogger_1.default.info("error: %j", err);
                }
            }
        });
    }
    formatPhaseToStringDefault(date) {
        const year = date.getFullYear();
        const month = date.getMonth();
        let season = "";
        switch (true) {
            case month < 3:
                season = "Q1";
                break;
            case month < 6:
                season = "Q2";
                break;
            case month < 9:
                season = "Q3";
                break;
            default:
                season = "Q4";
                break;
        }
        return `${year}${season}`;
    }
    formatPhaseToDate(OriginBasePhase, step, phase) {
        const basePhase = new Date(OriginBasePhase);
        const year = basePhase.getFullYear();
        const month = basePhase.getMonth();
        const date = basePhase.getDate();
        let newYear = year;
        let newMonth = month;
        let newDate = date;
        const unit = step.slice(-1);
        const stepNum = parseInt(step, 10);
        if (["y", "Y"].includes(unit)) {
            newYear = year + stepNum * phase;
            basePhase.setFullYear(newYear);
        }
        else if (["m", "M"].includes(unit)) {
            newMonth = month + stepNum * phase;
            basePhase.setMonth(newMonth);
        }
        else if (["w", "W"].includes(unit)) {
            newDate = date + stepNum * 7 * phase;
            basePhase.setFullYear(newYear);
        }
        else if (["d", "D"].includes(unit)) {
            newDate = date + stepNum * phase;
            basePhase.setDate(newDate);
        }
        return basePhase;
    }
    export2OssWithProject(projectId, phase, isReport) {
        return __awaiter(this, void 0, void 0, function* () {
            /**
             * 1. 找到当前Project下的，phase周期
             */
            const pm = new Project_1.default().getModel();
            const perm = new Period_1.default().getModel();
            const curProject = yield pm.findById(projectId).exec();
            const currentPhase = parseInt(phase, 10);
            const periodId = curProject.periods[currentPhase];
            const curPeriod = yield perm.findById(periodId).exec();
            /**
             * 2. 获取当前proposal
             */
            const psm = new Proposal_1.default().getModel();
            const proposalId = curProject.proposal;
            const curProposal = yield psm.findById(proposalId).exec();
            /**
             * 3. 获取当前的proposal下所有参与的hospital，products以及resources
             */
            const hsm = new Hospital_1.default().getModel();
            const hospIds = curProposal.targets;
            const condiHospIds = hospIds.map((x) => {
                return { _id: x };
            });
            const hospitals = yield hsm.find({ $or: condiHospIds }).exec();
            const prodsm = new Product_1.default().getModel();
            const prodIds = curProposal.products;
            const condiProdIds = prodIds.map((x) => {
                return { _id: x };
            });
            const products = yield prodsm.find({ $or: condiProdIds }).exec();
            const ressm = new Resource_1.default().getModel();
            const resIds = curProposal.resources;
            const condiResIds = resIds.map((x) => {
                return { _id: x };
            });
            const resources = yield ressm.find({ $or: condiResIds }).exec();
            let unSortData = [];
            let headers = [];
            const proposalCase = curProposal.case;
            if (isReport) {
                if (proposalCase === "ucb") {
                    headers = [
                        ["周期", "城市名称", "医院名称", "医院等级", "负责代表", "产品", "进药状态", "患者数量", "指标达成率", "销售额"]
                    ];
                }
                else if (proposalCase === "tm") {
                    headers = [
                        ["周期", "城市名称", "医院名称", "医院等级", "负责代表", "产品", "潜力", "指标达成率", "销售额"]
                    ];
                }
                /**
                 * 6. 从数据库中拉取数据Report
                 */
                const repsm = new Report_1.default().getModel();
                const presm = new Preset_1.default().getModel();
                const reports = yield repsm.find({
                    $or: [
                        { projectId },
                        { proposalId: proposalId.toString() }
                    ],
                    category: "Hospital",
                    phase: { $lt: currentPhase }
                }).sort("phase").exec();
                // const reports = preReports.concat(clacReports)
                const presets = yield presm.find({
                    $or: [
                        { projectId },
                        { proposalId: proposalId.toString() }
                    ],
                    category: 8,
                    phase: { $lte: currentPhase },
                });
                unSortData = reports.map((x, index) => {
                    const hospital = hospitals.find((h) => h.id === x.hospital.toString());
                    const tmprid = x.resource ? x.resource.toString() : "";
                    const resource = resources.find((r) => r.id === tmprid);
                    const product = products.find((p) => p.id === x.product.toString());
                    const condi = (pp) => {
                        if (x.phase < 0) {
                            return pp.phase - 1 === x.phase &&
                                pp.projectId === "" &&
                                pp.hospital.toString() === x.hospital.toString() &&
                                pp.product.toString() === x.product.toString();
                        }
                        else {
                            return pp.phase - 1 === x.phase &&
                                pp.projectId === projectId &&
                                pp.hospital.toString() === x.hospital.toString() &&
                                pp.product.toString() === x.product.toString();
                        }
                    };
                    const cpp = presets.find(condi);
                    let entrance = "";
                    if (cpp) {
                        if (cpp.currentDurgEntrance === "1") {
                            entrance = "已开发";
                        }
                        else if (cpp.currentDurgEntrance === "2") {
                            entrance = "正在开发";
                        }
                        else {
                            entrance = "未开发";
                        }
                    }
                    let pss = "";
                    pss = this.formatPhaseToStringDefault(this.formatPhaseToDate(curProposal.periodBase, curProposal.periodStep, x.phase));
                    switch (x.phase) {
                        case -4:
                            pss = "2018Q1";
                            break;
                        case -3:
                            pss = "2018Q2";
                            break;
                        case -2:
                            pss = "2018Q3";
                            break;
                        case -1:
                            pss = "2018Q4";
                            break;
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
                    const qFunc = (qa, q) => {
                        if (qa > 0) {
                            return qa.toFixed(3);
                        }
                        else if (q === 0) {
                            return 0;
                        }
                        else {
                            return 0;
                        }
                    };
                    const achiTMFunc = (sales, salesQuota) => {
                        if (salesQuota === 0) {
                            return 0;
                        }
                        else {
                            return (sales / salesQuota).toFixed(3);
                        }
                    };
                    let potentialOrPatient = 0;
                    let achi = null;
                    if (proposalCase === "ucb") {
                        const a = x.phase < 0 ? x.achievements : cpp.lastAchievement;
                        const b = x.phase < 0 ? x.salesQuota : cpp.lastQuota;
                        potentialOrPatient = cpp ? cpp.currentPatientNum : 0;
                        achi = qFunc(a, b);
                    }
                    else if (proposalCase === "tm") {
                        potentialOrPatient = cpp ? cpp.potential : 0;
                        achi = achiTMFunc(x.sales, x.salesQuota);
                    }
                    if (proposalCase === "ucb") {
                        return [
                            pss,
                            hospital.position,
                            hospital.name,
                            hospital.level,
                            resource ? resource.name : "未分配",
                            product.name,
                            entrance,
                            potentialOrPatient,
                            // tm 潜力, ucb 病患数量
                            // tslint:disable-next-line: max-line-length
                            achi,
                            x.sales ? x.sales.toFixed(0) : 0 // 9
                        ];
                    }
                    else if (proposalCase === "tm") {
                        return [
                            pss,
                            hospital.position,
                            hospital.name,
                            hospital.level,
                            resource ? resource.name : "未分配",
                            product.name,
                            potentialOrPatient,
                            // tm 潜力, ucb 病患数量
                            // tslint:disable-next-line: max-line-length
                            achi,
                            x.sales ? x.sales.toFixed(0) : 0 // 9
                        ];
                    }
                });
            }
            else {
                headers = [
                    ["周期", "代表", "医院", "产品名称", "销售指标分配", "预算分配"]
                ];
                /**
                 * inputReport
                 */
                const anssm = new Answer_1.default().getModel();
                const perIds = curProject.periods.map((x) => {
                    return { _id: x };
                });
                const allPeriods = yield perm.find({ $or: perIds }).exec();
                // tslint:disable-next-line: prefer-for-of
                for (let i = 0; i < allPeriods.length; i++) {
                    const phaseAnsIds = allPeriods[i].answers.map((x) => {
                        return { _id: x };
                    });
                    phLogger_2.default.info(phaseAnsIds);
                    const phaseAnswers = yield anssm.find({ $or: phaseAnsIds, category: "Business" }).exec();
                    const handledPhaseAnswers = phaseAnswers.map((ele, idx) => {
                        const hospital = hospitals.find((h) => h.id === ele.target.toString());
                        const resource = resources.find((r) => r.id === ele.resource.toString());
                        const product = products.find((p) => p.id === ele.product.toString());
                        return [
                            allPeriods[i].name,
                            resource ? resource.name : "未分配",
                            hospital.name,
                            product.name,
                            ele.salesTarget,
                            ele.budget
                        ];
                    });
                    unSortData = unSortData.concat(handledPhaseAnswers);
                }
            }
            // tm potential 2018Q1 2018Q2 2018Q3 <== 2018Q4
            if (proposalCase === "tm") {
                const Q4 = unSortData.filter((item) => item[0] === "2018Q4");
                const blankPotentialQ = unSortData.filter((item) => item[0] === "2018Q1" || item[0] === "2018Q2" || item[0] === "2018Q3");
                for (const row of Q4) {
                    const rowHospital = row[2];
                    const rowProduct = row[5];
                    const rowPotential = row[6];
                    const curRow = blankPotentialQ.filter((item) => item[2] === rowHospital && item[5] === rowProduct);
                    for (const blankP of curRow) {
                        blankP[6] = rowPotential;
                    }
                }
            }
            /**
             * 1. group by pss
             */
            const toPhase = ((x) => {
                return x[0];
            });
            const grouped = ramda_1.default.groupBy(toPhase, unSortData);
            let fr = [];
            for (const key of Object.keys(grouped)) {
                const rd = grouped[key];
                /**
                 * 2. to every phase, reduceBy hospital
                 */
                const toHos = ((x) => {
                    return x[2];
                });
                const hos = ramda_1.default.groupBy(toHos, rd);
                /**
                 * 2.1 sort in the hos
                 */
                // 7  ====> ucb patient
                // 6  ====> tm potential
                const sortFunc = (left, right) => {
                    const m = right[7] - left[7];
                    return m === 0 ? right[9] - left[9] : m;
                };
                const sortFuncTM = (left, right) => {
                    const m = right[6] - left[6];
                    return m === 0 ? right[8] - left[8] : m;
                };
                const nhos = Object.keys(hos).map((x) => {
                    if (proposalCase === "ucb") {
                        const ht = hos[x].sort(sortFunc);
                        return { key: x, lst: ht };
                    }
                    else if (proposalCase === "tm") {
                        const ht = hos[x].sort(sortFuncTM);
                        return { key: x, lst: ht };
                    }
                });
                const patNum = (acc, item) => acc += item[7];
                const potentialNum = (acc, item) => acc += item[6];
                const reduce = proposalCase === "ucb" ?
                    ramda_1.default.reduceBy(patNum, 0, toHos, rd) : ramda_1.default.reduceBy(potentialNum, 0, toHos, rd);
                /**
                 * 3. sort hospital in the phase
                 */
                const sortArr = Object.keys(reduce).map((x) => {
                    return { key: x, value: reduce[x] };
                });
                const sortedWithPat = ramda_1.default.sort((left, right) => right.value - left.value, sortArr);
                let result = [];
                sortedWithPat.forEach((item) => {
                    result = result.concat(nhos.find((x) => x.key === item.key).lst);
                });
                fr = fr.concat(result);
            }
            const data = headers.concat(fr);
            const jobId = v4_1.default();
            const workbook = XLSX.utils.book_new();
            const worksheet = XLSX.utils.aoa_to_sheet(data);
            workbook.Props = {
                Author: "Alfred Yang",
                CreatedDate: new Date(),
                Subject: "TM-Export",
                Title: jobId + this.suffix,
            };
            XLSX.utils.book_append_sheet(workbook, worksheet, "TM-Export");
            XLSX.writeFile(workbook, this.localPath + jobId + this.suffix);
            /**
             * 5. 链接oss
             */
            yield this.pushResult2OSS(jobId);
            return jobId;
        });
    }
}
exports.default = ExportProejct;
//# sourceMappingURL=ExportProject.js.map