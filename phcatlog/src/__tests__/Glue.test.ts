
import { GetDatabasesCommand, GlueClient } from "@aws-sdk/client-glue"
import {AssumeRoleCommand, STSClient} from "@aws-sdk/client-sts"

test("AWS-SDK Glue Get List", async () => {
    const client = new STSClient({
        region: "cn-northwest-1",
        credentials: {
            accessKeyId: "AKIAWPBDTVEAI6LUCLPX",
            secretAccessKey: "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",
        }
    })

    const params = {
        RoleArn: "arn:aws-cn:iam::444603803904:role/Pharbers-ETL-Roles",
        RoleSessionName: "Pharbers-ETL-Roles"
    }
    const command = new AssumeRoleCommand(params)

    try {
        const data = await client.send(command)
        // tslint:disable-next-line:no-console
        const glueClient = new GlueClient({
            region: "cn-northwest-1",
            credentials: {
                accessKeyId: data.Credentials.AccessKeyId,
                secretAccessKey: data.Credentials.SecretAccessKey,
                sessionToken: data.Credentials.SessionToken
            }
        })
        const glueCommand = new GetDatabasesCommand({})
        const response = await glueClient.send(glueCommand)
        // tslint:disable-next-line:no-console
        console.log(response.DatabaseList)
    } catch (error) {
        // tslint:disable-next-line:no-console
        console.error(error)
    } finally {
        // tslint:disable-next-line:no-console
        console.log("END")
        client.destroy()
    }

}, 1000 * 60 * 10)
