import {Logger} from "phnodelayer"

class Index {
    model: any = {
        project: {
            arn: String,
            name: String,
            provider: String,
            version: String,
            executions: { link: "execution", isArray: true, inverse: "projectExecution"}
        },
        execution: {
            projectExecution: { link: "project", inverse: "executions"},
            arn: String,
            input: String,
        },
        db: {
            name: String,
            provider: String,
            tables: { link: "table", isArray: true, inverse: "db" },
        },
        table: {
            name: String,
            database: String,
            provider: String,
            version: String,
            db: { link: "db", inverse: "tables" },
        }
    }

    operations = {
        hooks: {}
    }
}

export default Index