
class Entry {
    model: any = {
        asset: {
            name: String,
            owner: String,
            extension: String,
            size: Number,
            source: String,
            type: String, // candidate: database, file, stream, application, mart, cube
            accessibility: String,
            version: String,
            isNewVersion: Boolean,
            shared: String, // null => 未公开, Access => 公开成功, Applying => 审核正在公开中
            partners: String, // 对应公司ID
            providers: Array(String),
            markets: Array(String),
            molecules: Array(String),
            dateCover: Array(String),
            geoCover: Array(String),
            labels: Array(String),
            created: Date,
            modified: Date,
            description: String,
        }
    }

    operations = {
        hooks: {
            asset: [ this.hooksDate]
        }
    }

    protected hooksDate(context, record, update) {
        const { request: { method, meta: { language } } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                return record
        }
    }
}

export default Entry
