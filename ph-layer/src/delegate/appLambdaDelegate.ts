import { ServerResponse } from "http"
import fortuneHTTP from "../../lib/fortune-http"
import jsonApiSerializer from "../../lib/fortune-json-api"
import { StoreEnum } from "../common/StoreEnum"
import { ServerConf } from "../configFactory/serverConf"
import { SingletonInitConf } from "../configFactory/singletonConf"
import { StoreFactory } from "../dbFactory/StoreFactory"
import AWSReq from "../strategies/awsRequest"

/**
 * The summary section should be brief. On a documentation web site,
 * it will be shown on a page that lists summaries for many different
 * API items.  On a detail page for a single item, the summary will be
 * shown followed by the remarks section (if any).
 *
 */
export default class AppLambdaDelegate {
    public store: any
    public listener: any
    public isFirstInit = true
    private conf: ServerConf = new SingletonInitConf().getConf()

    public async prepare(se: StoreEnum) {
        this.store = StoreFactory.instance.getStore(se)
        await this.store.connect()
        this.isFirstInit = false
        this.listener = fortuneHTTP(this.store, {
            serializers: [
                [ jsonApiSerializer ]
            ]
        })
    }

    protected async cleanUp() {
        await this.store.disconnect()
    }

    protected async exec(event: Map<string, any>) {
        // @ts-ignore
        if ( !event.body ) {
            // @ts-ignore
            event.body = ""
        }
        const req = new AWSReq(event, this.conf.project)
        const response = new ServerResponse(req)
        // @ts-ignore
        const buffer = Buffer.from(event.body)
        // @ts-ignore
        req._readableState.buffer = buffer
        await this.listener(req, response, buffer)
        return response
    }
}
