import {
    GetDatabasesCommand,
    GetPartitionsCommand,
    GetTableCommand,
    GetTablesCommand} from "@aws-sdk/client-glue"

export default class GetGlueData {

    private static async getTablePartitionKeys(glueIns: any, databaseName: string, tableName: string) {
        const command = new GetTableCommand({
            DatabaseName: databaseName,
            Name: tableName
        })

        const result = await glueIns.getClient().send(command)
        return result.Table.PartitionKeys
    }

    async getDataBases(glueIns: any) {
        const command = new GetDatabasesCommand({})
        const result = await glueIns.getClient().send(command)
        return result.DatabaseList.map((item) => {
            return {
                id: item.Name,
                name: item.Name,
                describe: item.Description || ""
            }
        }).filter((item) => item.name !== "default")
    }

    async getTables(glueIns: any, databaseName: string) {
        function returnTableObject(table: any) {
            const partitionKeys = table.PartitionKeys.map((partition) => {
                return {
                    name: partition.Name,
                    type: partition.Type,
                    comment: partition.Comment || "",
                    parameters: partition.Parameters || ""
                }
            })
            const schemas = table.StorageDescriptor.Columns.map((col) => {
                return {
                    field: col.Name,
                    type: col.Type,
                    comment: col.Comment || "",
                    parameters: col.Parameters || ""
                }
            }).concat(partitionKeys.map((item) => {
                item["field"] = item.name
                delete item.name
                return item
            }))
            return {
                id: table.DatabaseName +  table.Name,
                name: table.Name,
                source: table.Location,
                partitionKeys ,
                schemas,
                describe: table.Description || "",
                connect: "",
                location: table.StorageDescriptor.Location,
                deprecated: table.Retention,
                lastModifyTime: table.UpdateTime.getTime(),
                inputFormat: table.StorageDescriptor.InputFormat,
                outputFormat: table.StorageDescriptor.OutputFormat,
                serdeLib: table.StorageDescriptor.SerdeInfo.SerializationLibrary,
                serdeArguments: table.StorageDescriptor.SerdeInfo.Parameters,
                tableAttributes: table.Parameters
            }
        }
        const command = new GetTablesCommand({
            DatabaseName: databaseName
        })
        const result = await glueIns.getClient().send(command)
        return result.TableList.map((table) => returnTableObject(table))
    }

    async getPartitions(glueIns: any, databaseName: string, tableName: string) {
        const partitionKeys = await GetGlueData.getTablePartitionKeys(glueIns, databaseName, tableName)
        const command = new GetPartitionsCommand({
            DatabaseName: databaseName,
            TableName: tableName
        })
        const result = await glueIns.getClient().send(command)
        return result.Partitions.map((item, index) => {
            const schema = {}
            item.Values.forEach((val, idx) => { schema[partitionKeys[idx].Name] = val })
            return { id: (databaseName + tableName + index), schema, attribute: JSON.stringify(item.StorageDescriptor) }
        })
    }
}
