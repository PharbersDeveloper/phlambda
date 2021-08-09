
class Project {
    model: any = {
        project: {
            arn: String,
            name: String,
            type: String,
            created: Number,
            provider: String,
            define: String,
            tags: Object,
        },
        execution: {
            arn: String,
            name: String,
            status: String,
            startTime: Number,
            endTime: Number,
            tags: Object
        }
    }

    operations = {
        hooks: {}
    }
}

export default Project
