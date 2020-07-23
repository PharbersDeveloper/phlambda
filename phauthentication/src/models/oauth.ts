
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
        accountRole: { link: "account", isArray: true, inverse: "defaultRole" },
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
        created: Date,
        expired: Date,
        registerRedirectUri: Array(String),
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
    }
    // authorization: {
    //     uid: String,
    //     cid: String,
    //     code: String,
    //     scope: String,
    //     create: Date,
    //     expired: Date
    // },
    // access: {
    //     uid: String,
    //     cid: String,
    //     token: String,
    //     refresh: String,
    //     create: Date,
    //     expired: Date
    // }
}

export default records
