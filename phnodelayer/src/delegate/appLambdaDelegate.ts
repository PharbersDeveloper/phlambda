import { ServerResponse } from "http"
import fortuneHTTP from "../../lib/fortune-http"
import jsonApiSerializer from "../../lib/fortune-json-api"
import { Adapter } from "../common/Adapter"
import { InitServerConf } from "../common/InitServerConf"
// import { StoreEnum } from "../common/StoreEnum"
import { ServerConf } from "../configFactory/ServerConf"
import DBFactory from "../dbFactory/DBFactory"
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
    private conf: ServerConf = InitServerConf.getConf

    public async prepare(name?: string) {
        // tslint:disable-next-line:no-unused-expression
        Adapter.init
        this.store = DBFactory.getInstance.getStore(name)
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
