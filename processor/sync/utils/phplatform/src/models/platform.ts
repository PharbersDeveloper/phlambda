import * as fortune from "fortune"

export default class Platform {
    model: any = {
        // 官网 开始
        activity: {
            title: String,
            subTitle: String,
            startDate: Date,
            endDate: Date,
            location: String,
            city: String,
            activityType: String,
            contentTitle: String,
            contentDesc: String,
            language: Number,
            logo: { link: "image", inverse: "actLogo" },
            logoOnTime: { link: "image", inverse: "actLogoOnTime" },
            gallery: { link: "image", isArray: true, inverse: "actGallery"},
            attachments: { link: "report", isArray: true, inverse: "actAttachments" },
            agendas: { link: "zone", isArray: true, inverse: "actAgendas" },
            partners: { link: "cooperation", isArray: true, inverse: "actPartners" }
        },
        image: {
            path: String,
            tag: String,
            actLogo: { link: "activity", isArray: true, inverse: "logo"},
            actLogoOnTime: { link: "activity", isArray: true, inverse: "logoOnTime"},
            actGallery: { link: "activity", isArray: true, inverse: "gallery"},
            rptCover: { link: "report", isArray: true, inverse: "cover"},
            partAvatar: { link: "participant", isArray: true, inverse: "avatar"},
            coLogo: { link: "cooperation", isArray: true, inverse: "logo"}
        },
        report: {
            title: String,
            subTitle: String,
            description: String,
            cover: { link: "image", inverse: "rptCover"},
            date: Date,
            language: Number,
            writers: { link: "participant", isArray: true, inverse: "writeReports"},
            actAttachments: { link: "activity", isArray: true, inverse: "attachments" },
        },
        participant: {
            name: String,
            title: String,
            occupation: String,
            language: Number,
            writeReports: { link: "report", isArray: true, inverse: "writers"},
            avatar: { link: "image", inverse: "partAvatar"},
            speak: { link: "event", isArray: true, inverse: "speakers"},
            host: { link: "zone", isArray: true, inverse: "hosts" }
        },
        cooperation: {
            name: String,
            companyType: String,
            logo: { link: "image", inverse: "coLogo" },
            language: Number,
            actPartners: { link: "activity", isArray: true, inverse: "partners" }
        },
        event: {
            title: String,
            subTitle: String,
            description: String,
            startDate: Date,
            endDate: Date,
            language: Number,
            speakers: { link: "participant", isArray: true, inverse: "speak" },
            hold: { link: "zone", inverse: "agendas" }
        },
        zone: {
            title: String,
            subTitle: String,
            description: String,
            startDate: Date,
            endDate: Date,
            language: Number,
            hosts: { link: "participant", isArray: true, inverse: "host" },
            agendas: { link: "event", isArray: true, inverse: "hold" },
            actAgendas: { link: "activity", inverse: "agendas" }
        },
        article: {
            title: String,
            date: Number,
            uri: String
        },
        // 官网 结束

        // 账户 开始
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
        apply: {
            company: String,
            department: String,
            email: String,
            intention: String,
            name: String,
            phone: String,
            position: String,
            create: Date
        },
        // 账户 结束

        file: {
            name: String,
            owner: String,
            extension: String,
            source: String,
            size: Number,
            version: String,
            labels: Array(String),
            created: Date,
            modified: Date,
            description: String,
        },
        project: {
            provider: String,
            name: String,
            owner: String,
            type: String,
            created: Date,
        },

        // configuration web pages
        page: {
            clientId: String,
            clientName: String,
            version: String,
            name: String,
            route: String,
            uri: String,
            cat: String,
            level: Number,
            engine: String
        },
        // configuration web layout
        layout: {
            clientId: String,
            clientName: String,
            version: String,
            name: String,
            css: String,
            script: String
        }
    }

    operations = {
        hooks: {
            file: [this.hooksDate],
            account: [ this.hookAccountInput, this.hookAccountOutput],
        }
    }

    verifyPassword(current: string, input: any): boolean {
        if (!input.replace.password) {
            return false
        }
        const spwd = input.replace.password.split("#")
        input.replace.password = spwd[1]
        return current === spwd[0]
    }

    protected hooksDate(context, record, update) {
        const { request: { method, meta: { language } } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.modified = date
                return record
            case "update":
                update.replace.modified = new Date()
                return update
        }
    }

    // Account Start
    protected hookAccountInput(context, record, update) {
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
                // 该操作为用户修改密码操作（登入系统后）
                update.replace.modified = new Date()
                if ("password" in update.replace && !this.verifyPassword(record.password, update)) {
                    throw new BadRequestError("Entered passwords differ")
                }
                return update
        }
    }

    protected hookAccountOutput(context, record) {
        delete record.password
        return record
    }
    // Account End
}
