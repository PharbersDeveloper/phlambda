import { CloudFormationClient, CreateStackCommand, DeleteStackCommand } from "@aws-sdk/client-cloudformation";

export default class OptCrawlerHandler {
    private client: CloudFormationClient = null

    constructor() {
        this.client = new CloudFormationClient({
            region: "cn-northwest-1"
        })
    }


    async create(id, tenant) {

        const s3Path = `s3://ph-platform/2020-11-11/lake/${tenant}/${id}/`

        const crawlerName = `crawler-${tenant}-${id}`

        const command = new CreateStackCommand({
            StackName: crawlerName,
            Parameters: [
                {
                    ParameterKey: "DatabaseName",
                    ParameterValue: id
                },
                {
                    ParameterKey: "CrawlerName",
                    ParameterValue: crawlerName
                },
                {
                    ParameterKey: "S3TargetPath",
                    ParameterValue: s3Path
                }
            ],
            TemplateURL:
                "https://ph-platform.s3.cn-northwest-1.amazonaws.com.cn/2020-11-11/cloudformation/glue/crawler/resourceCrawler.yaml"
        });
        await this.client.send(command);
    }

    async delete(id, tenant) {
        const crawlerName = `crawler-${tenant}-${id}`
        const command = new DeleteStackCommand({
            StackName: crawlerName
        })
        await this.client.send(command);
    }
}
