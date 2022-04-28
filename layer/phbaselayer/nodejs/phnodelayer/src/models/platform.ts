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
        diagram: {
            partner: String,
            name: String,
            source: String,
            rid: String,
            gid: String,
            tag: String,
            version: String,
            description: String,
            created: Date,
            modified: Date
        },
        db: { // 缺少Hook未写
            name: String,
            provider: String,
            tables: { link: "table", isArray: true, inverse: "db" },
            owner: Array(String), // Link To tenant Table ID（Logic）
        },
        table: {
            name: String,
            database: String,
            provider: String,
            version: String,
            db: { link: "db", inverse: "tables" },
        },
        resource: {
            name: String,
            resourceType: String, // 枚举值：暂时还可以是db、table、project、machine、jupyter
            created: Date,
            tenant: String, // Link To tenant Table ID（Logic）
            accounts: { link: "project", isArray: true, inverse: "owner" },
            concrets: Array(String), // Link To table or project Table ID（Logic）
        },
        project: {
            provider: String,
            name: String,
            owner: { link: "resource", isArray: false, inverse: "accounts", }, // Link 一对一
            type: String, // saas 无 Flow  pass有Flow
            created: Date,
            models: { link: "model", isArray: true, inverse: "project" }, // Link 一对多
            scripts: { link: "script", isArray: true, inverse: "project" }, // Link 一对多
            datasets: { link: "dataset", isArray: true, inverse: "project" }, // Link 一对多
            flow: { link: "flow", isArray: false, inverse: "project" }, // Link 一对一
            analysis: { link: "analysis", isArray: false, inverse: "project", }, // Link 一对一
            notebooks: { link: "notebook", isArray: true, inverse: "project"}, // Link 一对多
            dashBoards: { link: "dashBoard", isArray: true, inverse: "project" }, // Link 一对多
            wikis: { link: "wiki", isArray: true, inverse: "project" }, // Link 一对多
            tasks: Array(String), // 暂时不做
            actions: Array(String) // 原样不动，详细的actions根据project id带入到DynamoDB中去查找
        },
        model: {
            project: { link: "project", isArray: false, inverse: "models" },
            name: String,
            type: String,
            location: String,
            definition: String, // JSON String
        },
        script: {
            project: { link: "project", isArray: false, inverse: "scripts" },
            type: String,
            name: String,
            inputDfs: { link: "dataset", isArray: true, inverse: "scriptInput" },
            outputDfs: { link: "dataset", isArray: true, inverse: "scriptOutput" },
            args: String,
            reverse: String,
            stateDisplay: { link: "stateDisplay", isArray: false, inverse: "startScripts" },
        },
        dataset: {
            project: { link: "project", isArray: false, inverse: "datasets" },
            scriptInput: { link: "script", isArray: false, inverse: "inputDfs" },
            scriptOutput: { link: "script", isArray: false, inverse: "outputDfs" },
            type: String,
            name: String,
            displayName: String,
            connectConfig: String, // JSON String
            secretConfig: String, // JSON String
            schema: String, // JSON String
        },
        flow: {
            project: { link: "project", isArray: false, inverse: "flow" },
            stateMachines: { link: "stateMachine", isArray: true, inverse: "flow" }
        },
        stateMachine: {
            flow: { link: "flow", isArray: false, inverse: "stateMachines" },
            type: String, // 分为AirFlow或Step Function
            // arn: String,
            name: String, // 如果是AirFLow name = DAGName|StepFunction name = arn
            project: String, // 外链project id
            displayName: String,
            display: { link: "stateDisplay", isArray: false, inverse: "stateMachine" },
            // version: String,
        },
        stateDisplay: {
            stateMachine: { link: "stateMachine", isArray: false, inverse: "display" },
            name: String,
            definition: String, // JSON String
            startScripts: { link: "script", isArray: true, inverse: "stateDisplay" },
        },
        analysis: { // 原计划绑定resource（租户共享资源），现阶段硬件资源全部绑定到project中，这里先空着
            project: { link: "project", isArray: false, inverse: "analysis"},
            name: String
        },
        notebook: {
            project: { link: "project", isArray: false, inverse: "notebooks"},
            name: String,
            url: String,
            type: String,
            resource: String // 原计划绑定resource（租户共享资源），现阶段硬件资源全部绑定到project中，这里先空着
        },
        dashBoard: {
            project: { link: "project", isArray: false, inverse: "dashBoards" },
            slides: { link: "slide", isArray: true, inverse: "dashBoard" },
        },
        slide: {
            dashBoard: { link: "dashBoard", isArray: false, inverse: "slides" },
            chats: { link: "chat", isArray: true, inverse: "slide" }
        },
        chat: {
            slide: { link: "slide", isArray: false, inverse: "chats" },
        },
        wiki: {
            project: { link: "project", isArray: false, inverse: "wikis" },
            type: String, // MD or HTML
            location: String
        },

        // configuration web pages
        page: {
            cliendId: String,
            clientName: String,
            version: String,
            name: String,
            route: String,
            uri: String,
            cat: String,
            level: Number,
            engine: String
        }
    }

    operations = {
        hooks: {
            file: [this.hooksDate],
            diagram: [this.hooksDate],
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

    protected hooksDate(context: any, record: any, update: any) {
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
    protected hookAccountInput(context: any, record: any, update: any) {
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

    protected hookAccountOutput(context: any, record: any, update: any) {
        delete record.password
        return record
    }
    // Account End
}
