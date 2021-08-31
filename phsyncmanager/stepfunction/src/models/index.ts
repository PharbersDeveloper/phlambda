import {Logger} from "phnodelayer"

class Index {
    model: any = {
        project: {
            arn: String,
            name: String,
            projectName: String,
            provider: String,
            version: String,
            executions: { link: "execution", isArray: true, inverse: "projectExecution"}
        },
        execution: {
            projectExecution: { link: "project", inverse: "executions"},
            arn: String,
            input: String,
        },
    }

    operations = {
        hooks: {}
    }
}

export default Index
