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
        hooks: { }
    }
}

export default Max
