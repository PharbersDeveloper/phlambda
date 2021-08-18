import StepFunctionHandler from "./StepFunctionHandler"

export default class GetStepLogs {
    private stf = new StepFunctionHandler()
    private AccessKeyId = "AKIAWPBDTVEAI6LUCLPX"
    private SecretAccessKey = "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"

    async FindMapReduceLogs(arn: string, name: string) {
        const events = (await this.stf.findEventHistory(arn)).filter((item) => item.name === name)
        let count = events.length
        const results = []
        while (count > 0) {
            const event = events.pop()
            const obj = "ouput" in event.value ? JSON.parse(event.value.output) : event.value
            if (event.type === "TaskStateExited") {
                results.push({
                    clusterId: obj.clusterId,
                    stepId: obj.firstStep.StepId,
                    type: "s3"
                })
            } else if (event.type.search("Failed") > -1) {
                results.push({
                    clusterId: obj?.clusterId || "",
                    stepId: obj?.firstStep?.StepId || "",
                    error: obj?.error || "",
                    cause: obj?.cause || "",
                    type: "error" in obj ? "string" : "s3"
                })
            }
            count = events.length
        }
        return results
    }
}
