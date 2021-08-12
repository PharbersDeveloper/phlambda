import GlueCatlogHandler from "../handler/GlueCatlogHandler"

class Catlog {
    model: any = {
        db: {
            name: String,
            provider: String,
            tables: { link: "table", isArray: true, inverse: "db" },
        },
        table: {
            name: String,
            database: String,
            provider: String,
            version: String,
            isNewVersion: Boolean,
            // partitionCount: Number,
            db: { link: "db", inverse: "tables" },
        }
    }

    operations = {
        hooks: {
            db: [null, this.hookDataBaseOutput],
            table: [null, this.hookTableOutput],
        }
    }

    protected async hookDataBaseOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const gch = new GlueCatlogHandler()
                const content = await gch.findDatabase(record.name)
                record.created = content.Database.CreateTime.getTime()
                record.description = content.Database.Description || ""
        }
        return record
    }

    protected async hookTableOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const gch = new GlueCatlogHandler()
                const content = await gch.findTable(record.database, record.name)
                record.created = content.Table.CreateTime.getTime()
                record.updated = content.Table.UpdateTime.getTime()
                record.retention = content.Table.Retention
                record.cloumns = content.Table.StorageDescriptor.Columns
                record.location = content.Table.StorageDescriptor.Location
                record.inputFormat = content.Table.StorageDescriptor.InputFormat
                record.outputFormat = content.Table.StorageDescriptor.OutputFormat
                record.compressed = content.Table.StorageDescriptor.Compressed
                record.serdeInfo = content.Table.StorageDescriptor.SerdeInfo
                record.bucketColumns = content.Table.StorageDescriptor.BucketColumns
                record.sortColumns = content.Table.StorageDescriptor.SortColumns
                record.parameters = content.Table.Parameters
                record.partitionKeys = content.Table.PartitionKeys
                record.tableType = content.Table.TableType
                record.isRegisteredWithLakeFormation = content.Table.IsRegisteredWithLakeFormation
        }
        return record
    }
}

export default Catlog
