class Max {
    model: any = {
        project: {
            provider: String,
            time: Number,
            actions: String
        },
        jobLog: {
            provider: String,
            owner: String,
            showName: String,
            time: Number,
            version: String,
            code: Number,
            jobDesc: String,
            jobCat: String,
            comments: String,
            message: String,
            date: Number
        }
    }

    operations = {
        hooks: {
            project: [this.hookProjectInput]
        }
    }

    protected async hookProjectInput(context, record, update) {
        const { request: { method } } = context
        switch (method) {
            case "update":
                const value = JSON.parse(update.replace.actions)
                const actions = JSON.parse(record.actions)
                    .filter((item) => item.jobCat !== value.jobCat)
                actions.push(value)
                update.replace.actions = JSON.stringify(actions)
                return update
        }
    }

}

export default Max
