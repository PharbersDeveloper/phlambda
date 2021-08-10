import StepFunctionHandler from "../handler/StepFunctionHandler"

class Project {
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
            name: String,
        }
    }

    operations = {
        hooks: {
            project: [null, this.hookProjectOutput],
            execution: [null, this.hookExecutionOutput]
        }
    }

    protected async hookProjectOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const stp = new StepFunctionHandler()
                const content = await stp.findStepFunctions(record.arn)
                record["type"] = content.type
                record["created"] = content.creationDate.getTime()
                record["define"] = JSON.stringify(JSON.parse(content.definition))
        }
        return record

    }

    protected async hookExecutionOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                const stp = new StepFunctionHandler()
                const content = await stp.findExecutions(record.arn)
                record.status = content.status
                record.startTime = content.startDate.getTime()
                record.stopDate = content.stopDate.getTime()
                record.input = content.input
        }
        return record

    }

}

export default Project
