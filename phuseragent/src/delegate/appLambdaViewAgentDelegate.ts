// import phS3Facade from "../s3facade/phS3Facade"
import * as fs from "fs"
import phLogger from "../logger/phLogger"
import AppLambdaDelegate from "./appLambdaDelegate"

export default class AppLambdaViewAgentDelegate extends AppLambdaDelegate {
    public async exec(event: Map<string, any>) {
        const res = await super.exec(event)
        // TODO: 暂时注释掉
        // @ts-ignore
        // const data = String(res.output[1])
        // const hbs = JSON.parse(data).data.attributes.hbs
        // const result = await phS3Facade.getObject("ph-cli-dag-template", hbs)
        // @ts-ignore
        // res.output[1] = result.toString()
        const hbs =  fs.readFileSync("config/login.hbs")
        phLogger.log(String(hbs))
        // @ts-ignore
        res.output[1] = String(hbs)
        // @ts-ignore
        res.headers = { "content-type": "text/x-handlebars-template" }
        return res
    }

    public prepare() {
        super.prepare()
    }

    public async cleanUp() {
        await super.cleanUp()
    }

}
