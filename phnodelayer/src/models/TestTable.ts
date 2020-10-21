class TestTable {
    public model: any = {
        event: {
            name: String,
            time: Date
        }
    }

    public operations = {
        hooks: {
            event: [ this.hooksDate ]
        }
    }

    protected hooksDate(context, record, update) {
        const { request: { method, meta: { language } } } = context

        switch (method) {
            case "create":
                record.time = new Date()
                return record
        }
    }
}

export default TestTable
