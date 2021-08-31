
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
        },
        dataBlock: {
            assetBlock: {link: "asset", inverse: "block"},
            dfs: {link: "dataSet", isArray: true, inverse: "blockDs"},
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
            sampleData: {link: "dataSetSample", isArray: true, inverse: "ds"},
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
            ds: {link: "dataSet", inverse: "sampleData"},
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
        productcategory: {
            category: String,
            type: String,
            level: Number,
            value: String,
            description: String,
            version: String,
            products: { link: "product", isArray: true, inverse: "category" },
        },
        productrelationship: {
            category: String,
            type: String,
            value: String,
            version: String,
            products: { link: "product", isArray: true, inverse: "packId" },
        },
        lexicon: {
            category: String,
            type: String,
            encode: Number,
            value: String,
            version: String,
        },
        product: {
            moleName: String,
            prodDesc: String,
            prodNameCh: String,
            pack: String,
            pckDesc: String,
            dosage: String,
            contains: { link: "molespec", isArray: true, inverse: "products" },
            spec: String,
            mnfId: { link: "manufacturer", inverse: "products" },
            category: { link: "productcategory", isArray: true, inverse: "products" },
            packId: { link: "productrelationship", inverse: "products" },
            events: String,
        },
        molespec: {
            products: {link: "product", isArray: true, inverse: "contains"},
            type: String,
            moleName: String,
            quantity: String,
            unit: String,
        },
        manufacturer: {
            products: {link: "product", isArray: true, inverse: "mnfId"},
            mnfNameCh: String,
            mnfType: String,
            mnfTypeName: String,
            mnfTypeNameCh: String,
            corpId: String,
            corpNameEn: String,
            corpNameCh: String,
            location: Array(String),
            version: String
        },
        description: {
            name: String,
            source: String,
            format: String,
            createTime: Date,
            version: String
        },
        // dbSource: {
        //     dbType: String,
        //     url: String,
        //     user: String,
        //     pwd: String,
        //     dbName: String,
        //     create: Date,
        //     assetDbs: { link: "asset", inverse: "dbs" }
        // },
    }

    public operations = {
        hooks: {
            asset: [ this.hooksDate],
            dataSet: [ this.hooksDate ],
            dataSetSample: [ this.hooksDate ],
            job: [ this.hooksDate ]
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
            case "update":
                update.replace.modified = new Date()
                return update
        }
    }
}

export default Entry
