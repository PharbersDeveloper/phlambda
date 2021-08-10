
class Catlog {
    model: any = {
        database: {
            name: String,
            provider: String,
            version: String,
            isNewVersion: Boolean,
            partitionCount: Number,
            tables: { link: "table", isArray: true, inverse: "db" },
        },
        table: {
            name: String,
            db: { link: "database", inverse: "tables" },
        },
        partition: { // 逻辑抽象，实际数据库会有一条假数据，与链表的辅助头节点原理一致，只是为了能更好的处理数据
            name: String
        }
    }

    operations = {
        hooks: {
            database: [null, this.hookDataBaseOutput]
        }
    }

    protected async hookDataBaseOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        return record
    }

}

export default Catlog
