
export interface IIdentify {
    verify(event: Map<string, any>, scope: string): boolean
}

enum permissions {
    ALL = "*",
    Write = "w",
    Read = "r",
    Exec = "x",
    A = "a"
}

export default class Identify implements IIdentify {
    httpMethod: Map<string, string[]> = new Map<permissions, string[]>()

    constructor() {
        this.httpMethod.set(permissions.Read, ["get"])
        this.httpMethod.set(permissions.Write, ["get", "post", "patch"])
        this.httpMethod.set(permissions.Exec, ["get", "delete"])
        this.httpMethod.set(permissions.A, ["get", "post", "patch", "delete"])
    }

    verify(event: Map<string, any>, scope: string = "APP|phcommon:accounts:qtaGDePl1OrSFEgm:W,phcommon:parthers:psNeInomlGaSfgvd:R|W#APP|entry:assets&filter[parthers]=psNeInomlGaSfgvd:*:R,entry:assets&filter[owner]=qtaGDePl1OrSFEgm:*:W|W#APP|reports:parthers:5xeiSaYk_1noz-RKPyJ8:R,reports:templates:fVxL1xByKMkIAW1ct_su:R|R"): boolean {
        if (!scope) return false
        const method = event["httpMethod"].toLowerCase()
        const paths = event["path"].split("/").filter((s: string) => s !== "")
        let splitScope = scope.split("#")
        // 如果是super admin scope = * 全权限 access
        if (splitScope.length === 1 && splitScope[0] === permissions.ALL) return true

        splitScope = splitScope.filter(item => item.includes(paths[0]))
        const initScope = splitScope.shift().split("|")

        // 如果是平台全权限 admin scope = APP|*|权限，需验证operation是否符合权限
        if (initScope.length === 3 && initScope[1] === permissions.ALL
            && this.httpMethod.get(initScope[2].toLowerCase()).includes(method)) return true

        // APP|phcommon:accounts:qtaGDePl1OrSFEgm:W,phcommon:parthers:psNeInomlGaSfgvd:R|W
        // APP|entry:assets&filter[parthers]=psNeInomlGaSfgvd:*:R,entry:assets&filter[owner]=qtaGDePl1OrSFEgm:*:W|W

        const url = Object.keys(event["queryStringParameters"]).map((key: string) => {
            if ("ids[]" in event["multiValueQueryStringParameters"]
                && event["multiValueQueryStringParameters"]["ids[]"].length === 1) {
                event["pathParameters"] = Object.assign(event["pathParameters"], {id: event["multiValueQueryStringParameters"]["ids[]"][0]})
            }
            return `${paths[1]}&${key}=${event["queryStringParameters"][key]}`
        })

        const detailARN = initScope[1].split(",")
        const flag = detailARN.map((arn: string) => {
            const detail = arn.split(":")
            if ((detail[1] === permissions.ALL || detail[2] === permissions.ALL)
                && this.httpMethod.get(detail[3].toLowerCase()).includes(method)) {
                return true
            }
            if ("id" in event["pathParameters"]) {
                return detail[1] === paths[1]
                    && event["pathParameters"].id === detail[2]
                    && this.httpMethod.get(detail[3].toLowerCase()).includes(method)
            }
            return this.httpMethod.get(detail[3].toLowerCase()).includes(method)
                && detail[1].split("&")[0] === paths[1]
                && url.includes(detail[1])
        })

        if (flag.includes(true)) return true

        return this.verify(event, splitScope.join("#"))
    }
}
