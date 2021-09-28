import StepFunctionHandler from "../handler/StepFunctionHandler"

class Project {
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
        }
    }

    operations = {
        hooks: {
            project: [null, this.hookProjectOutput],
            execution: [this.hookExecutionInput, this.hookExecutionOutput]
        }
    }

    protected async hookProjectOutput(context, record) {
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        switch (method) {
            case "find":
                if (record.arn) {
                    const stp = new StepFunctionHandler()
                    const content = await stp.findStepFunctions(record.arn)
                    record.type = content.type
                    record.created = content.creationDate.getTime()
                    record.define = JSON.stringify(JSON.parse(content.definition))
                }
        }
        return record

    }

    protected async hookExecutionInput(context, record) {
        const { request: { method, type } } = context
        const stp = new StepFunctionHandler()
        switch (method) {
            case "create":
                if (record.input) {
                    const {result, input} = await stp.startExecution(record.input)
                    record.arn = result.executionArn
                    record.input = input
                }
                return record
        }
        return record
    }

    protected async hookExecutionOutput(context, record) {
        const { request: { method, type } } = context
        switch (method) {
            case "find":
                if (record.arn) {
                    const stp = new StepFunctionHandler()
                    const content = await stp.findExecutions(record.arn)
                    record.name = record.arn.split(":").slice(-1)[0]
                    record.status = content.status
                    record.startTime = content.startDate.getTime()
                    record.stopTime = content.stopDate === undefined ? -1 : content.stopDate.getTime()
                    record.input = JSON.stringify(content.input)
                }
                break
        }
        return record

    }

}

export default Project
