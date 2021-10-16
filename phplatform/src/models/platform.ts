
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
        file: {
            name: String,
            owner: String,
            extension: String,
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
            accounts: Array(String),
            concrets: Array(String), // Link To table or project Table ID（Logic）
        },
        project: {
            name: String,
            owner: String,
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
            actions: Array(String) // Link 一对多 DynamoDB
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
            arn: String,
            name: String,
            project: String, // 外链project id
            display: { link: "stateDisplay", isArray: false, inverse: "stateMachine" },
            version: String,
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
        }

    }

    operations = {
        hooks: {
            diagram: [ this.hooksDate ]
        }
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
}
