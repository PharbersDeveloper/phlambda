
const records = {
    account: {
        name: String,
        email: String,
        password: String,
        phoneNumber: String,
        wechatOpenId: String,
        defaultRole: { link: "role", inverse: "accountRole" },
        employer: { link: "partner", inverse: "employee" }
    },
    role: {
        name: String,
        description: String,
        scope: { link: "scope", isArray: true, inverse: "owner" },
        accountRole: { link: "account", inverse: "defaultRole" },
    },
    scope: {
        name: String,
        description: String,
        scopePolicy: String,
        owner: { link: "role", isArray: true, inverse: "scope" }
    },
    partner: {
        name: String,
        address: String,
        phoneNumber: String,
        web: String,
        employee: { link: "account", isArray: true, inverse: "employer" }
    },
    client: {
        name: String,
        description: String,
        secret: String,
        clientComponents: { link: "component", isArray: true, inverse: "client" }
    },
    component: {
        name: String,
        title: String,
        description: String,
        created: Date,
        updated: Date,
        hbs: String,
        version: String,
        client: { link: "client", isArray: true, inverse: "clientComponents" }
    },
}

export default records
