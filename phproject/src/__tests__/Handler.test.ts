import StepFunctionHandler from "../handler/StepFunctionHandler"

process.env.AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
process.env.SecretAccessKey = "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"

describe("Handler Test", () => {

    test("start execution", async () => {
        const sfh = new StepFunctionHandler()
        const input = {
            dag_name: "ETL_Iterator",
            parameters: [
                {
                    p_input: "s3://ph-max-auto/v0.0.1-2020-06-08/Common_files/extract_data_files/MAX_city_normalize.csv",
                    p_output: "s3://ph-platform/2020-11-11/etl/readable_files/test",
                    g_partition: "provider, version",
                    g_filldefalut: "provider:common,version:20210623_u0079u0079u0077,owner:pharbers",
                    g_bucket: "NONE",
                    g_mapping: "NONE",
                    type: "csv"
                },
                {
                    p_input: "s3://ph-max-auto/v0.0.1-2020-06-08/奥鸿/202012/prod_mapping",
                    p_output: "s3://ph-platform/2020-11-11/etl/readable_files/test",
                    g_partition: "provider, version",
                    g_filldefalut: "provider:奥鸿,version:202012_u0079u0079u0077,owner:pharbers",
                    g_bucket: "NONE",
                    g_mapping: "NONE",
                    type: "parquet"
                }
            ]
        }
        await sfh.startExecution(JSON.stringify(input))
    }, 1000 * 60 * 10)

})
