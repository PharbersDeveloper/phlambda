class Reports {
    public model: any = {
        template: {
            parent: { link: "template", isArray: true, inverse: "child" },
            child: { link: "template", isArray: true, inverse: "parent" },
            partnerTemplate: {link: "partner", inverse: "templates"},
            name: String,
            source: String,
            rid: String,
            gid: String,
            tag: String,
            version: String,
            description: String,
            created: Date,
            modified: Date
        },
        partner: {
            pid: String,
            templates: { link: "template", isArray: true, inverse: "partnerTemplate" },
            created: Date,
            modified: Date
        }
    }

    public operations = {
        hooks: {
            template: [ this.hooksDate ],
            partner: [ this.hooksDate ]
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

export default Reports
