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
            provider: String,
            version: String,
            isNewVersion: Boolean,
            partitionCount: Number,
            db: { link: "db", inverse: "tables" },
        },
        partition: { // 逻辑抽象，实际数据库会有一条假数据，与链表的辅助头节点原理一致，只是为了能更好的处理数据
            name: String
        }
    }

    operations = {
        hooks: {
            db: [null, this.hookDataBaseOutput],
            table: [null, this.hookTableOutput],
            partition: [null, this.hookPartition]
        }
    }

    protected async hookDataBaseOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const gch = new GlueCatlogHandler()
                const content = await gch.findDatabase("")
                record.created = ""
        }
        return record
    }

    protected async hookTableOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const gch = new GlueCatlogHandler()
                const content = await gch.findTable("", "")
                record.created = ""
        }
        return record
    }

    protected async hookPartition(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const gch = new GlueCatlogHandler()
                const content = await gch.findPartitions("", "", "")
                record.created = ""
        }
        return record
    }

}

export default Catlog
