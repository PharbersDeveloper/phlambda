
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

    verify(event: Map<string, any>, scope: string): boolean {
        if (!scope) return false
        const method = event["httpMethod"].toLowerCase()
        const paths = event["path"].split("/").filter((s: string) => s !== "")
        let splitScope = scope.split("#")
        // 如果是super admin scope = * 全权限 access
        if (splitScope.length === 1 && splitScope[0] === permissions.ALL) return true

        splitScope = splitScope.filter(item => item.includes(paths[0]) || (item.includes("*") && item.split("|")[1].length === 1))
        if (splitScope.length === 0) return false
        const initScope = splitScope.shift().split("|")

        // 如果是平台全权限 admin scope = APP|*|权限，需验证operation是否符合权限
        if (initScope.length === 3 && initScope[1] === permissions.ALL
            && this.httpMethod.get(initScope[2].toLowerCase()).includes(method)) return true

        const url = Object.keys(event["queryStringParameters"]).map((key: string) => {
            // TODO 专门为前端不好的查询习惯兼容代码
            if ("ids[]" in event["multiValueQueryStringParameters"]
                && event["multiValueQueryStringParameters"]["ids[]"].length === 1) {
                event["pathParameters"] = Object.assign(event["pathParameters"], {id: event["multiValueQueryStringParameters"]["ids[]"][0]})
            } else if("filter[id]" in event["queryStringParameters"]) {
                event["pathParameters"] = Object.assign(event["pathParameters"], {id: event["queryStringParameters"]["filter[id]"]})
            }
            return `${paths[1]}&${key}=${event["queryStringParameters"][key]}`
        })

        const detailARN = initScope[1].split(",")
        const flag = detailARN.map((arn: string) => {
            const detail = arn.split(":")
            if ((detail[1] === permissions.ALL || (!detail[1].includes("&") && detail[2] === permissions.ALL))
                && this.httpMethod.get(detail[3].toLowerCase()).includes(method)) {
                return true
            }
            if ("id" in event["pathParameters"] && !detail[1].includes("&")) {
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
