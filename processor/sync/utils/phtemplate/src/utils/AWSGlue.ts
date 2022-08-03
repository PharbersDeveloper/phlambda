import { GlueClient } from "@aws-sdk/client-glue"
import { AWSRegion } from "../constants/common"
import STS from "./AWSSts"

export default class AWSGlue {
    private readonly client: any = null
    // private client: any = null

    constructor() {
        this.client = new GlueClient({
            region: AWSRegion
        })
    }

    getClient() {
        // const sts =
        //     new STS("AKIAWPBDTVEAI6LUCLPX", "Efi6dTMqXkZQ6sOpmBZA1IO1iu3rQyWAbvKJy599", AWSRegion)
        // let config = await sts.assumeRole("Pharbers-ETL-Roles",
        // "arn:aws-cn:iam::444603803904:role/Pharbers-ETL-Roles")
        // this.client = new GlueClient(config)
        return this.client
    }

    destroy() {
        this.client.destroy()
    }
}
