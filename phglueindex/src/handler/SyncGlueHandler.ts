import {PutItemCommand} from "@aws-sdk/client-dynamodb"
import {
    GetTableCommand,
    paginateGetPartitions
} from "@aws-sdk/client-glue"
import {IStore, Logger} from "phnodelayer"
import AWSDynamoDB from "../utils/AWSDynamoDB"
import AWsGlue from "../utils/AWSGlue"
import ObjectUtil from "../utils/ObjectUtil"
import GlueHandler from "./GlueHandler"

export default class SyncGlueHandler extends GlueHandler {
    private backRWConfig: any

    constructor(store: IStore, config: any, backRWConfig: any) {
        super(store, config)
        this.backRWConfig = backRWConfig
    }

    async syncPartition2DynamoDB(dbName: string, tableName: string) {
        const instance = new AWsGlue(this.config)
        const client = instance.getClient()
        const dyClient = new AWSDynamoDB(this.backRWConfig).getClient()
        const command = new GetTableCommand({
            DatabaseName: dbName,
            Name: tableName
        })
        const tableResult = await client.send(command)
        const partitionKeys = tableResult?.Table?.PartitionKeys?.map((item) => item.Name) || [ObjectUtil.generateId()]
        const pagePartition = await paginateGetPartitions({client}, {
            DatabaseName: dbName,
            TableName: tableName
        })
        for await (const item of pagePartition) {
            for (const record of item.Partitions) {
                const partitionCommand = new PutItemCommand({
                    Item: {
                        id: {
                            S: ObjectUtil.generateId(),
                        },
                        smID: {
                            S: tableName,
                        },
                        source: {
                            S: record.StorageDescriptor.Location
                        },
                        schema: {
                            S: JSON.stringify(record.StorageDescriptor.Columns)
                        },
                        date: {
                            N: record.CreationTime.getTime().toString()
                        },
                        partitions: {
                            S: JSON.stringify(record.Values)
                        }
                    },
                    TableName: "partition"
                })
                await dyClient.send(partitionCommand)
            }
        }
    }
}
