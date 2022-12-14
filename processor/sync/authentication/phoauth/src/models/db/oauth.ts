class OAuth {
    model: any = {
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
            notification: { link: "notification", isArray: false, inverse: "account" },
            defaultRole: { link: "role", inverse: "accountRole" },
            employer: { link: "partner", inverse: "employee" },
        },
        notification: {
            notificationPolicy: String, // JSON String
            notificationType: String,
            account: { link: "account", isArray: false, inverse: "notification" }
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
            owner: { link: "role", isArray: true, inverse: "scope" },
        },
        partner: {
            name: String,
            address: String,
            phoneNumber: String,
            web: String,
            created: Date,
            modified: Date,
            employee: { link: "account", isArray: true, inverse: "employer" },
        },
        client: {
            name: String,
            description: String,
            secret: String,
            created: Date,
            expired: Date,
            registerRedirectUri: Array(String),
            domain: Array(String),
            clientComponents: { link: "component", isArray: true, inverse: "client" },
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
        },
    }
}
export default OAuth
