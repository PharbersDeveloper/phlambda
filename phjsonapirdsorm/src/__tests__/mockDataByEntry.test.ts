// import { dbFactory, logger } from "phnodelayer"
//
// test("Mock Entry Data", async () => {
//     logger.info("Init")
//
//     const store = dbFactory.getInstance.getStore()
//     const aid = "zH3pZyugPW15eT6h"
//     const dbid = "rbaesu6SnyLdg5cR"
//     const dsid = "rbaesu6dasbnjadn"
//     const asset = {
//         id: aid,
//         name: "CPA不标准事实表",
//         owner: "auto robot",
//         extension: "",
//         size: -1,
//         source: "",
//         type: "fact", // candidate: database, file, stream, application, mart, cube
//         accessibility: "r",
//         version: "0.0.22",
//         isNewVersion: true,
//         providers: ["*"],
//         markets: ["*"],
//         molecules: ["*"],
//         dateCover: ["*"],
//         geoCover: ["*"],
//         labels: ["*"],
//         description: "CPA不标准事实表",
//     }
//     const dbBlock = {
//         id: dbid,
//         dfs: [dsid],
//         assetBlock: aid,
//         name: "CPA",
//         label: "",
//         type: "fact",
//         description: "CPA不标准事实表"
//     }
//     const ds = {
//         id: dsid,
//         name: "CPA不标准事实表",
//         schema: ["SALES_QTY_BOX:string",
//             "SALES_QTY_GRAIN:string",
//             "SALES_QTY_TAG:string",
//             "SALES_VALUE:string",
//             "version:string",
//             "CPA_PROD_ID:long",
//             "CPA_HOSP_ID:long",
//             "CPA_DATE_ID:long",
//             "A_ETC_ID:long"],
//         source: "2020-08-10/datamart/original/fact_tables/cpa/v0.0.22_20201020_1",
//         storeType: "parquet",
//         size: 38353558,
//         description: "CPA Original Fact Table"
//     }
//     await store.create("asset", asset)
//     await store.create("dataSet", ds)
//     await store.create("dataBlock", dbBlock)
//     await store.disconnect()
//     logger.info("End")
// })
