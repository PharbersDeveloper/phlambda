
export class JSONAPIAdapter {
    // TODO: 这边该规定类型才对，偷懒了，还有这边应该注册不同adapter，不然达不到效果，所以我又偷懒了
    private readonly data: any = null
    private readonly type: string = ""

    constructor(type, data) {
        this.data = data
        this.type = type
    }

    serialize() {
        const table = this.data?.Table || undefined
        const attributes = {}
        attributes["name"] = table.Name
        attributes["created"] = table.CreateTime.getTime()
        attributes["updated"] = table.UpdateTime.getTime()
        attributes["retention"] = table.Retention
        attributes["columns"] = table.StorageDescriptor.Columns
        attributes["location"] = table.StorageDescriptor.Location
        attributes["inputFormat"] = table.StorageDescriptor.InputFormat
        attributes["outputFormat"] = table.StorageDescriptor.OutputFormat
        attributes["compressed"] = table.StorageDescriptor.Compressed
        attributes["serdeInfo"] = table.StorageDescriptor.SerdeInfo
        attributes["bucketColumns"] = table.StorageDescriptor.BucketColumns
        attributes["sortColumns"] = table.StorageDescriptor.SortColumns
        attributes["parameters"] = table.Parameters
        attributes["partitionKeys"] = table.PartitionKeys
        attributes["tableType"] = table.TableType
        attributes["isRegisteredWithLakeFormation"] = table.IsRegisteredWithLakeFormation

        return {
            data: {
                id: new Date().getTime(),
                attributes,
                type: this.type,
            },
            meta: {}
        }
    }
}
