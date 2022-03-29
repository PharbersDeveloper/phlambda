
class Entry {
    model: any = {
        asset: {
            name: String,
            owner: String,
            extension: String,
            size: Number,
            source: String,
            version: String,
            partners: String, // 对应公司ID
            labels: Array(String),
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
        }
    }

    operations = {
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
