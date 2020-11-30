
export interface IIdentify {
    verify(scope: string, event: Map<string, any>): boolean
}

enum permissions {
    ALL = "*",
    Write = "w",
    Read = "r",
    Exec = "x"
}

export default class Identify implements IIdentify {
    httpMethod: Map<string, string[]> = new Map<permissions, string[]>()

    constructor() {
        this.httpMethod.set(permissions.Read, ["get"])
        this.httpMethod.set(permissions.Write, ["get", "post", "patch"])
        this.httpMethod.set(permissions.Exec, ["get", "delete"])
    }

    verify(scope: string = "APP|phcommon:accounts:qtaGDePl1OrSFEgm:W,phcommon:parthers:psNeInomlGaSfgvd:R|W#APP|entry:assets&filter[parthers]=psNeInomlGaSfgvd:*:R,entry:assets&filter[owner]=qtaGDePl1OrSFEgm:*:W|W#APP|reports:parthers:5xeiSaYk_1noz-RKPyJ8:R,reports:templates:fVxL1xByKMkIAW1ct_su:R|R", event: Map<string, any>): boolean {
        const method = event["httpMethod"].toLowerCase()
        const paths = event["path"].split("/").filter((s: string) => s !== "")
        const splitScope = scope.split("#")
        // 如果是super admin scope = * 全权限 access
        if (splitScope.length === 1 && splitScope[0] === permissions.ALL) return true

        const initScope = splitScope.shift().split("|")

        // 如果是平台全权限 admin scope = APP|*|权限，需验证operation是否符合权限
        if (initScope.length === 3 && initScope[1] === permissions.ALL
            && this.httpMethod.get(initScope[2].toLowerCase()).includes(method)) return true

        // APP|phcommon:accounts:qtaGDePl1OrSFEgm:W,phcommon:parthers:psNeInomlGaSfgvd:R|W
        // APP|entry:assets&filter[parthers]=psNeInomlGaSfgvd:*:R,entry:assets&filter[owner]=qtaGDePl1OrSFEgm:*:W|W

        const detailARN = initScope[1].split(",")
        detailARN.map((arn: string) => {
            const detail = arn.split(":")
            if (detail[1].split("&")[0] === permissions.ALL) {

            }
            return this.httpMethod.get(detail[3].toLowerCase()).includes(method)
                && detail[0] === paths[0]
                && detail[1].split("&")[0] === paths[1]
                && true
        })

        return this.verify(splitScope.join("#"), event)
    }
}
