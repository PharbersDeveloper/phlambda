import {
    GetDatabasesCommand,
    GetPartitionsCommand,
    GetTableCommand,
    GetTablesCommand} from "@aws-sdk/client-glue"

export default class GetGlueData {

    public async getDataBases(glueIns: any) {
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

    public async getTables(glueIns: any, databaseName: string) {
        function returnTableObject(table: any) {
            return {
                id: table.DatabaseName +  table.Name,
                name: table.Name,
                source: table.Location,
                schemas: table.StorageDescriptor.Columns.map((col) => {
                    return { field: col.Name, type: col.Type }
                }),
                describe: "",
                connect: "",
                deprecated: table.Retention,
                lastModifyTime: table.LastAccessTime,
                inputFormat: table.StorageDescriptor.InputFormat,
                outputFormat: table.StorageDescriptor.OutputFormat,
                serdeLib: table.StorageDescriptor.SerdeInfo.SerializationLibrary,
                serdeArguments: table.StorageDescriptor.SerdeInfo.Parameters,
                sizeKey: table.Parameters.sizeKey,
                objectCount: table.Parameters.objectCount,
                updateByCrawler: table.Parameters.UPDATED_BY_CRAWLER,
                crawlerSchemaSerializerVersion: table.Parameters.CrawlerSchemaSerializerVersion,
                crawlerSchemaDeserializerVersion: table.Parameters.CrawlerSchemaDeserializerVersion,
                recordCount: table.Parameters.recordCount,
                averageRecordSize: table.Parameters.averageRecordSize,
                compressionType: table.Parameters.compressionType,
                typeOfData: table.Parameters.typeOfData,
            }
        }
        const command = new GetTablesCommand({
            DatabaseName: databaseName
        })
        const result = await glueIns.getClient().send(command)
        return result.TableList.map((table) => returnTableObject(table))
    }

    public async getPartitions(glueIns: any, databaseName: string, tableName: string) {
        const partitionKeys = await this.getTablePartitionKeys(glueIns, databaseName, tableName)
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

    private async getTablePartitionKeys(glueIns: any, databaseName: string, tableName: string) {
        const command = new GetTableCommand({
            DatabaseName: databaseName,
            Name: tableName
        })

        const result = await glueIns.getClient().send(command)
        return result.Table.PartitionKeys
    }
}
