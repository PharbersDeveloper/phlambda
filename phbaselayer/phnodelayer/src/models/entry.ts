
class Entry {
    public model: any = {
        asset: {
            name: String,
            block: { link: "dataBlock", isArray: true, inverse: "assetBlock" },
            owner: String,
            extension: String,
            size: Number,
            source: String,
            type: String, // candidate: database, file, stream, application, mart, cube
            accessibility: String,
            version: String,
            isNewVersion: Boolean,
            providers: Array(String),
            markets: Array(String),
            molecules: Array(String),
            dateCover: Array(String),
            geoCover: Array(String),
            labels: Array(String),
            created: Date,
            modified: Date,
            description: String,
        },
        dataBlock: {
            assetBlock: { link: "asset", inverse: "block" },
            dfs: { link: "dataSet", isArray: true, inverse: "blockDs" },
            name: String,
            label: String,
            startRow: Number,
            type: String,
            description: String,
        },
        dataSet: {
            parent: { link: "dataSet", isArray: true, inverse: "child" },
            child: { link: "dataSet", isArray: true, inverse: "parent" },
            blockDs: { link: "dataBlock", inverse: "dfs" },
            sampleData: { link: "dataSetSample", isArray: true, inverse: "ds" },
            job: { link: "job", inverse: "gen" },
            name: String,
            schema: Array(String),
            source: String,
            storeType: String,
            size: Number,
            created: Date,
            modified: Date,
            description: String,
        },
        dataSetSample: {
            ds: { link: "dataSet", inverse: "sampleData" },
            data: String,
            created: Date,
            modified: Date,
            description: String,
        },
        job: {
            gen: { link: "dataSet", isArray: true, inverse: "job" },
            task: String,
            inputDS: Array(String),
            outPutDS: Array(String),
            jobId: String,
            asset: String,
            status: String,
            start: Date,
            end: Date,
            created: Date,
            modified: Date,
            description: String,
        },
    }

    public operations = {
        hooks: {
            asset: [ this.hooksDate ]
        }
    }

    public hooksDate(context: any, record: any, update: any) {
        const { request: { method, meta: { language } } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                return record
            case "update":
                update.replace.modified = new Date()
                return update
        }
    }
}

export default Entry
