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
        const stp = new StepFunctionHandler()
        switch (method) {
            case "find":
                if (type === "project") {
                    const content = await stp.findStepFunctions(record.arn)
                    record["type"] = content.type
                    record["created"] = content.creationDate.getTime()
                    record["define"] = JSON.stringify(JSON.parse(content.definition))
                }
        }
        return record

    }

    protected async hookExecutionOutput(context, record) {
        function delObjectOfNull(obj) {
            Object.keys(obj).map((item) => {
                if (!obj[item]) {
                    delete obj[item]
                }
                return true
            })
        }
        const { request: { method, type } } = context
        const { request: { uriObject: { query }} } = context
        const stp = new StepFunctionHandler()
        switch (method) {
            case "find":
                if (type === "execution") {
                    const content = await stp.findExecutions(record.arn)
                    const historyEvents = await stp.findEventHistory(record.arn)
                    for (const item of historyEvents.events) {
                        delObjectOfNull(item)
                    }
                    record.status = content.status
                    record.startTime = content.startDate.getTime()
                    record.stopDate = content.stopDate.getTime()
                    record.input = content.input
                    record.events = historyEvents.events
                }
        }
        return record

    }

}

export default Project
