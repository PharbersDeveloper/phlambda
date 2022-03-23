import IStrategy from "../common/IStrategy"

export default class MapReduceLogsHandler implements IStrategy {
    private readonly AccessKeyId
    private readonly SecretAccessKey
    private readonly emrLogLocation = "s3://ph-platform/2020-11-11/emr/logs/{clusterId}/steps/{stepId}/{content}"

    constructor(AccessKeyId: string, SecretAccessKey: string) {
        this.AccessKeyId = AccessKeyId
        this.SecretAccessKey = SecretAccessKey
    }

    async extractLog(events: any[]) {
        let count = events.length
        const results = []
        while (count > 0) {
            const event = events.pop()
            const obj = "output" in event.value ? JSON.parse(event.value.output) : event.value
            // 改成正则
            if (event.type === "TaskStateExited") {
                results.push({
                    source: this.emrLogLocation
                        .replace("{clusterId}", obj.clusterId)
                        .replace("{stepId}", obj.firstStep.StepId)
                        .replace("{content}", "controller.gz"),
                    type: "s3"
                })
            } else if (event.type === "TaskSubmitFailed") {
                results.push({
                    error: obj?.error || "",
                    cause: obj?.cause || "",
                    type: "string"
                })
            } else if (event.type === "TaskFailed") {
                results.push({
                    source: JSON.parse(obj.cause)?.Step?.Status?.FailureDetails?.LogFile || "",
                    type: "s3"
                })
            }
            count = events.length
        }

        return {
            AccessKeyId: this.AccessKeyId,
            SecretAccessKey: this.SecretAccessKey,
            results
        }
    }
}
