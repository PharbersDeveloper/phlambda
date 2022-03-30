import sqs from "aws-sdk/clients/sqs"

class SQSFacade {
    private sqs

    constructor(options: any) {
        this.sqs = new sqs(options)
    }

    public send(message: any) {
        return this.sqs.sendMessage(message).promise()
    }
}

export default SQSFacade
