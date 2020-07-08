import phS3Facade from "../s3facade/phS3Facade"
import AppLambdaDelegate from "./appLambdaDelegate"

export default class AppLambdaViewAgentDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const res = await super.exec(event)
        // @ts-ignore
        const data = String(res.output[1])
        const hbs = JSON.parse(data).data.attributes.hbs
        const result = await phS3Facade.getObject("ph-cli-dag-template", hbs)
        // @ts-ignore
        res.output[1] = result.toString()
        // @ts-ignore
        res.headers = { "content-type": "text/x-handlebars-template"}
        return res
    }
}
