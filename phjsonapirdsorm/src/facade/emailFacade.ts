import SQSFacade from "../facade/sqsFacade"

class EmailFacade {
    private sqs
    constructor(sqs: any) {
        this.sqs = sqs
    }
    public async sendEmail(to: string, subject: string, contentType: string, content: string) {
       return await this.sqs.send({
            MessageBody: process.env.MESSAGEBODY,
            QueueUrl: process.env.QUEUEURL,
            MessageAttributes: {
                To: {
                    DataType: "String",
                    StringValue: to
                },
                Subject: {
                    DataType: "String",
                    StringValue: subject || process.env.SUBJECT
                },
                ContentType: {
                    DataType: "String",
                    StringValue: contentType
                },
                Content: {
                    DataType: "String",
                    StringValue: content
                },
            },
            MessageGroupId: new Date().getTime().toString(),
            MessageDeduplicationId: new Date().getTime().toString()
        })
    }
}
export default EmailFacade
