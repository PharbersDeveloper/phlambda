
class Project {
    model: any = {
        project: {
            name: String,
            type: String,
            created: Number,
            provider: String,
            tags: Object,
        }
    }

    operations = {
        hooks: {}
    }
}

export default Project
