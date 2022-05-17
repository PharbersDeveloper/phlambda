class Common {

    public model: any = {
        account: {
            email: String,
            password: String
        }
    }

    public operations = {
        hooks: {
            account: [ this.input, this.output]
        }
    }

    protected input(context, record, update) {
        const { request: { method } } = context
        switch (method) {
            case "update":
                update.replace.modified = new Date()
                return update
        }
    }

    protected output(context, record) {
        delete record.password
        return record
    }
}

export default Common
