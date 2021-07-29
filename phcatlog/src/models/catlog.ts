
class Catlog {
    model: any = {
        database: {
            name: String,
            // tables: { link: "table", isArray: true, inverse: "db" },
            describe: String,
        },
        table: {
            name: String,
            schemas: Object,
            describe: String,
            source: String,
            connect: String,
            category: String,
            location: String,
            deprecated: String,
            lastModifyTime: String,
            inputFormat: String,
            outputFormat: String,
            serdeLib: String,
            serdeArguments: Object,
            tableAttributes: Object,
            partitionKeys: Object,
            // db: { link: "database", inverse: "tables" },
            // partitions: { link: "partition", isArray: true, inverse: "tablePartition" },
        },
        partition: {
            // tablePartition: { link: "table", inverse: "partitions" },
            schema: String,
            attribute: String
        }
    }

    operations = {
        hooks: {}
    }
}

export default Catlog
