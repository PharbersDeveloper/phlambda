import {
    GetDatabaseCommand,
    GetPartitionsCommand,
    GetTableCommand,
    paginateGetPartitions
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

    async findPartitions(databaseName: string, name: string, nextToken: string, size: number) {
        const sts =  new AWSSts(process.env.AccessKeyId, process.env.SecretAccessKey)
        const config = await sts.assumeRole()
        const instance = await new AWsGlue(config)
        const client = instance.getClient()
        const table = await this.findTable(databaseName, name)
        const partitions = table.Table.PartitionKeys
        const partitionCount = table.Table.Parameters.partitionCount || 0
        const content = await paginateGetPartitions({
            client,
            pageSize: size,
            startingToken: nextToken
        }, {
            DatabaseName: databaseName,
            TableName: name
        })

        let currentData = []
        let pageToken = nextToken === "" ? [""] : []
        let skipData = false
        if (nextToken === "") {
            for await (const item of content) {
                pageToken.push(item.NextToken)
                if (!skipData) {
                    currentData = item.Partitions.map((partition, index) => {
                        const schema = {}
                        partition.Values.forEach((val, idx) => { schema[partitions[idx].Name] = val })
                        return { schema, attribute: JSON.stringify(partition.StorageDescriptor) }
                    })
                }
                skipData = true
            }
        } else {
            const next = (await content.next())
            currentData = next.value.Partitions.map((partition, index) => {
                const schema = {}
                partition.Values.forEach((val, idx) => { schema[partitions[idx].Name] = val })
                return { schema, attribute: JSON.stringify(partition.StorageDescriptor) }
            })
        }

        instance.destroy()
        return {
            pageToken,
            content: currentData,
            count: partitionCount
        }
    }
}
