import {
    GetDatabaseCommand,
    GetPartitionsCommand,
    GetTableCommand
} from "@aws-sdk/client-glue"
import AWsGlue from "../utils/AWSGlue"
import AWSSts from "../utils/AWSSts"

export default class GlueCatlogHandler {

    async findDatabase(name: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = await new AWsGlue(config)
        const client = instance.getClient()
        const command = new GetDatabaseCommand({
            Name: name
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }

    async findTable(databaseName: string, name: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = await new AWsGlue(config)
        const client = instance.getClient()
        const command = new GetTableCommand({
            DatabaseName: databaseName,
            Name: name
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }

    async findPartitions(databaseName: string, name: string, nextToken: string) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = await new AWsGlue(config)
        const client = instance.getClient()
        const command = new GetPartitionsCommand({
            DatabaseName: databaseName,
            TableName: name,
            NextToken: nextToken
        })
        const content = await client.send(command)
        instance.destroy()
        return content
    }
}
