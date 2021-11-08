import { DBConfig, IStore, Logger, Register, ServerRegisterConfig, StoreEnum } from "phnodelayer"
import { Permissions, PostgresConf, RedisConf } from "../constants/common"

export default class AppLambdaDelegate {
    private readonly pg: IStore
    private readonly rds: IStore

    public constructor() {
        const configs = [
            new DBConfig(PostgresConf),
            new DBConfig(RedisConf)
        ]
        ServerRegisterConfig(configs)
        this.pg = Register.getInstance.getData(StoreEnum.POSTGRES) as IStore
        this.rds = Register.getInstance.getData(StoreEnum.REDIS) as IStore
    }

    public async exec(event: any) {
        try {
            await this.rds.open()
            return await this.authHandler(event)
        } catch (e) {
            throw e
        } finally {
            await this.rds.close()
        }
    }

    protected async authHandler(event: Map<string, any>) {
        // @ts-ignore
        const token = event.authorizationToken
        const result = await this.rds.find("access", null, { match: { token } })
        const records = result.payload.records
        // @ts-ignore
        const arnList = event.methodArn.split(":")
        const resourceList = arnList[5].split("/")
        if (records.length === 0) {
            // @ts-ignore
            return this.generatePolicy("undefined", "Deny", event.methodArn)
        }
        const scopes = records[0].scope.split("|")
        if (scopes.length === 1 && scopes[0] === "*") {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Allow", event.methodArn)
        }
        const auth = records[0].scope.split("#").map((item) => {
            return this.identify(resourceList, item)
        })
        if ([].concat(...auth).includes(true)) {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Allow", event.methodArn)
        } else {
            // @ts-ignore
            return this.generatePolicy(records[0].uid, "Deny", event.methodArn)
        }
    }

    protected identify(arnRes: string[], scope: string) {
        const outerScope = scope.split("|")
        const scopes = outerScope[1].split(",")

        function permissionFlag(permission) {
            // R => Read   W => R + Update + Create   X => R + Delete   A => 所有权限
            if (permission === "A") {
                return true
            }
            const pem = Permissions.map((item) => {
                if (item[0] === "W" || item[0] === "X") {
                    const read = Permissions.find((p) => p[0] === "R").substr(1)
                    return Permissions.find((p) => p[0] === item[0]) + read
                } else {
                    return item
                }
            })
            return pem
                .find((item) => permission === item[0])
                .split("::")
                .includes(arnRes[2])
        }

        function resourceFlag() {
            if (scopes.length === 1 && scopes[0] === "*") { return permissionFlag(outerScope[2])}
            return scopes.map((sc: string) => {
                const resource = sc.split(":")
                let temp = true
                if (resource[2] !== "*" && arnRes.length >= 6) {
                    temp = arnRes[5] === resource[2]
                }
                if (arnRes[4]){
                    return arnRes[3] === resource[0] &&
                        resource[1].includes(arnRes[4]) && temp && permissionFlag(resource[resource.length - 1])
                } else {
                    return arnRes[3] === resource[0] && temp && permissionFlag(resource[resource.length - 1])
                }

            })
        }
        return resourceFlag()
    }

    protected generatePolicy(principalId, effect, resource) {
        const authResponse = {}
        // @ts-ignore
        authResponse.principalId = principalId
        if (effect && resource) {
            // @ts-ignore
            const policyDocument = {}
            // @ts-ignore
            policyDocument.Version = "2012-10-17"
            // @ts-ignore
            policyDocument.Statement = []
            const statementOne = {}
            // @ts-ignore
            statementOne.Action = "execute-api:Invoke"
            // @ts-ignore
            statementOne.Effect = effect
            // @ts-ignore
            statementOne.Resource = resource
            // @ts-ignore
            policyDocument.Statement[0] = statementOne
            // @ts-ignore
            authResponse.policyDocument = policyDocument
        }
        return authResponse
    }

}
