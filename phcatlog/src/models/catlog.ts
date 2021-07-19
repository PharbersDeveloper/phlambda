
class Catlog {
    public model: any = {
        database: {
            name: String,
            tables: { link: "table", isArray: true, inverse: "db" },
            describe: String,
        },
        table: {
            name: String,
            schemas: Object,
            db: { link: "database", inverse: "tables" },
            partitions: { link: "partition", isArray: true, inverse: "tablePartition" },
            info: { link: "basicInfo", isArray: false, inverse: "tableBasicInfo" }
        },
        basicInfo: {
            tableBasicInfo: { link: "table", inverse: "info" },
            source: String,
            connect: String,
            deprecated: String,
            modifyTime: String,
            inputFormat: String,
            outputFormat: String,
            serdeLib: String,
            serdeArguments: String,
            sizeKey: String,
            objectCount: String,
            updateByCrawler: String,
            crawlerSchemaSerializerVersion: String,
            recordCount: String,
            averageRecordSize: String,
            crawlerSchemaDeserializerVersion: String,
            compressionType: String,
            typeOfData: String
        },
        partition: {
            tablePartition: { link: "table", inverse: "partitions" },
            field: String,
            value: String,
            attribute: String
        }
    }

    public operations = {
        hooks: {}
    }
}

export default Catlog
