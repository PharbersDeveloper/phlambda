// 'use strict';
//
// const phLogger = require("phnodelayer").phLogger
// const DBFactory = require("phnodelayer").DBFactory
//
// const fortune = require("fortune")
// const PostgresAdapter = require("fortune-postgres")
// let pg;
// let pg2;
//
// describe('convert data', function () {
//     before('init', async () => {
//         const url = "postgres://pharbers:Abcde196125@ph-db-lambda.cngk1jeurmnv.rds.cn-northwest-1.amazonaws.com.cn:5432/phentry"
//         const record = {
//             // test Fix Bug PBDP-401: add fileIndex for the upload files'
//             // TODO: will gen another bug for the new version & is new version
//             oldfileIndex: {
//                 fileName: String,
//                 owner: Array(String),
//                 martTags: Array(String),
//                 providers: Array(String),
//                 markets: Array(String),
//                 molecules: Array(String),
//                 dataCover: Array(String),
//                 geoCover: Array(String),
//                 labels: Array(String),
//                 assets: { link: "oldasset", isArray: true, inverse: "fi" }
//             },
//             oldfile: {
//                 fileName: String,
//                 sheetName: String,
//                 startRow: Number,
//                 label: String,
//                 extension: String,
//                 size: Number,
//                 url: String,
//                 assetFile: { link: "oldasset", inverse: "file" }
//             },
//             job: {
//                 codeProvider: String,
//                 codeRepository: String,
//                 codeBranch: String,
//                 codeVersion: String,
//                 jobContainerId: String,
//                 create: Date,
//                 description: String,
//                 gen: { link: "olddataSet", inverse: "job" }
//             },
//             dbSource: {
//                 dbType: String,
//                 url: String,
//                 user: String,
//                 pwd: String,
//                 dbName: String,
//                 create: Date,
//                 assetDbs: { link: "oldasset", inverse: "dbs" }
//             },
//             olddataSet: {
//                 colNames: Array(String),
//                 length: Number,
//                 url: String,
//                 description: String,
//                 tabName: String,
//                 status: String,
//                 parent: { link: "olddataSet", isArray: true, inverse: "child" },
//                 child: { link: "olddataSet", isArray: true, inverse: "parent" },
//                 job: { link: "job", inverse: "gen" },
//                 mart: { link: "mart", inverse: "dfs" },
//                 assetDs: { link: "oldasset", inverse: "dfs" }
//             },
//             mart: {
//                 dfs: { link: "olddataSet", isArray: true, inverse: "mart" },
//                 name: String,
//                 url: String,
//                 dataType: String,
//                 description: String,
//                 assetMart: { link: "oldasset", inverse: "mart" }
//             },
//             oldasset: {
//                 name: String,
//                 description: String,
//                 owner: String,
//                 accessibility: String,
//                 version: String,
//                 isNewVersion: Boolean,
//                 dataType: String, // candidate: database, file, stream, application, mart, cube
//                 fi: { link: "oldfileIndex", inverse: "assets" },
//                 file: { link: "oldfile", inverse: "assetFile" },
//                 dbs: { link: "dbSource", inverse: "assetDbs" },
//                 dfs: { link: "olddataSet", isArray: true, inverse: "assetDs" },
//                 mart: { link: "mart", inverse: "assetMart" },
//                 martTags: Array(String),
//                 providers: Array(String),
//                 markets: Array(String),
//                 molecules: Array(String),
//                 dataCover: Array(String),
//                 geoCover: Array(String),
//                 labels: Array(String),
//                 createTime: Date
//             }
//         }
//         pg = fortune(record, {adapter: [ PostgresAdapter, {url}]})
//         pg2 = DBFactory.getInstance.getStore()
//     })
//
//
//     it ('c', async () => {
//         const asset = await pg.find("oldasset")
//         const assetRes = asset.payload.records
//         const file = await pg.find("oldfile")
//         const fileRes = file.payload.records
//         const ds = await pg.find("olddataSet")
//         const dsRes = ds.payload.records
//
//         // 排除asset中的mart数据 & 是最新可用版本的File类型
//         const a1 = assetRes.filter(item => item.dataType !== "mart" && item.isNewVersion === true)
//         // group by name 得到有多少个block，对应关系，进行转换赋值
//         const a2 = a1.reduce((r, a) => {
//             r[a.name] = r[a.name] || []
//             r[a.name].push(a)
//             return r
//         }, Object.create(null))
//
//         for (const key in a2) {
//             const a3 = a2[key][0]
//             const blockIds = await Promise.all(a2[key].map( async ass => {
//                 const fileFind = fileRes.find(file => file.id === ass.file)
//                 const filterDS = ass.dfs.map( dfs => {
//                     const findDs = dsRes.find(item => item.id === dfs)
//                     return {
//                         id: findDs.id,
//                         parent: findDs.parent,
//                         sampleData: [],
//                         name: findDs.tabName,
//                         schema: findDs.colNames,
//                         source: findDs.url,
//                         storeType: "parquet",
//                         size: findDs.length,
//                         created: new Date(),
//                         modified: new Date(),
//                         description: findDs.description,
//                     }
//                 })
//                 for (const n of filterDS) {
//                     await pg2.create("dataSet", n)
//                 }
//
//                 const block = {
//                     id: fileFind.id,
//                     dfs: filterDS.map(item => item.id),
//                     name: fileFind.sheetName,
//                     label: fileFind.label,
//                     startRow: fileFind.startRow,
//                     type: "file",
//                     description: "",
//                 }
//                 await pg2.create("dataBlock", block)
//                 return block.id
//             }))
//             phLogger.info(blockIds)
//
//             const file = fileRes.find(item => item.id === a3.file)
//
//             const newAsset = {
//                 id: a3.id,
//                 name: a3.name,
//                 block: blockIds,
//                 owner: a3.owner,
//                 extension: file.extension,
//                 size: file.size || -1,
//                 source: file.url || "",
//                 type: a3.dataType,
//                 accessibility: a3.accessibility,
//                 version: a3.version,
//                 isNewVersion: a3.isNewVersion,
//                 providers: a3.providers,
//                 markets: a3.markets,
//                 molecules: a3.molecules,
//                 dateCover: a3.dataCover,
//                 geoCover: a3.geoCover,
//                 labels: a3.labels,
//                 created: a3.createTime,
//                 modified: new Date(),
//                 description: a3.description
//             }
//
//             phLogger.info(newAsset)
//             await pg2.create("asset", newAsset)
//         }
//     })
//
//     after("close db", async () => {
//         // pg.disconnect()
//         // pg2.disconnect()
//     });
//
// });