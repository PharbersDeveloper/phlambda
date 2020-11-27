import * as fortune from "fortune"

class Common {

    private static verifyPassword(current: string, input: any): boolean {
        if (!input.replace.password) {
            return false
        }
        const spwd = input.replace.password.split("#")
        input.replace.password = spwd[1]
        return current === spwd[0]
    }

    public model: any = {
        account: {
            name: String,
            firstName: String,
            lastName: String,
            email: String,
            password: String,
            phoneNumber: String,
            wechatOpenId: String,
            created: Date,
            modified: Date,
            defaultRole: { link: "role", inverse: "accountRole" },
            employer: { link: "partner", inverse: "employee" }
        },
        role: {
            name: String,
            description: String,
            created: Date,
            modified: Date,
            scope: { link: "scope", isArray: true, inverse: "owner" },
            accountRole: { link: "account", isArray: true, inverse: "defaultRole" },
        },
        scope: {
            name: String,
            description: String,
            scopePolicy: String,
            created: Date,
            modified: Date,
            owner: { link: "role", isArray: true, inverse: "scope" }
        },
        partner: {
            name: String,
            address: String,
            phoneNumber: String,
            web: String,
            created: Date,
            modified: Date,
            employee: { link: "account", isArray: true, inverse: "employer" }
        },
        client: {
            name: String,
            description: String,
            secret: String,
            created: Date,
            modified: Date,
            clientComponents: { link: "component", isArray: true, inverse: "client" }
        },
        component: {
            name: String,
            title: String,
            description: String,
            created: Date,
            modified: Date,
            hbs: String,
            version: String,
            client: { link: "client", isArray: true, inverse: "clientComponents" },
        }
    }

    public operations = {
        hooks: {
            account: [ this.input, this.output],
            role: [ this.input ],
            scope: [ this.input ],
            partner: [ this.input ],
            client: [ this.input ],
            component: [ this.input ]
        }
    }

    protected input(context, record, update) {
        const { errors: { BadRequestError } } = fortune
        const { request: { method } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                if (!record.name) {
                    record.name = record.email.split("@")[0]
                }
                if (!record.firstName || !record.lastName) {
                    throw new BadRequestError("FirstName Or LastName Can Not Be Empty")
                }
                return record
            case "update":
                update.replace.modified = new Date()
                if ("password" in update.replace && !Common.verifyPassword(record.password, update)) {
                    throw new BadRequestError("Entered passwords differ")
                }
                return update
        }
    }

    protected output(context, record) {
        delete record.password
        return record
    }
}

export default Common
