import fs from "fs"

export default class Register {

    private static instance: Register = null
    private entity: any = null
    private func: Map<string, any> = new Map()
    private constructor() {}

    registerEntity(entity: string) {
        if (!this.entity) {
            this.entity = new (this.createModel(entity))()
        }
        return this
    }

    registerFunction(model: string, func: any) {
        this.func.set(model, func)
        return this
    }

    getEntity() {
        return this.entity
    }

    getFunc(entity: string) {
        return this.func.get(entity)
    }

    static get getInstance() {
        if (Register.instance === null) {
            Register.instance = new Register()
        }
        return Register.instance
    }

    private createModel(entity: string) {
        const base = process.cwd()
        fs.statSync(`${base}/dist/models`)
        return require(`${base}/dist/models/${entity}.js`).default
    }
}
