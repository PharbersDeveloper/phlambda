
import { GetDatabasesCommand, GlueClient } from "@aws-sdk/client-glue"
import { AssumeRoleCommand, STSClient } from "@aws-sdk/client-sts"
import { AWsGlue } from "../utils/AWSGlue"
import { AWSSts } from "../utils/AWSSts"

test("AWS-SDK Glue Get List", async () => {
    try {
        // const sts = new AWSSts()
        // const result = await sts.assumeRole("AKIAWPBDTVEAI6LUCLPX",
        //     "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599")

        // const glue = new AWsGlue(result.AccessKeyId, result.SecretAccessKey, result.SessionToken)
        // const listDataBase = await glue.getDataBases()
        // const listTables = await glue.getTables("phdatacat")
        // console.info(JSON.stringify(listDataBase))
        // console.info(JSON.stringify(listTables, null, "  "))

        // const partition = await glue.getPartitions("phdatacat", "chemdata")
        // console.info(JSON.stringify(partition, null, "  "))

    } catch (error) {
        console.info(error)
    }
}, 1000 * 60 * 10)
