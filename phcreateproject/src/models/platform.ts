import * as fortune from "fortune"
import OptEfsHandler from "../handler/optEfsHandler"
import ObjectUtil from "../utils/ObjectUtil"

export default class Platform {
    model: any = {

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
        }
    }

    operations = {
        hooks: {
            project: [ this.hookProjectInput ],
        }
    }

    protected hookProjectInput(context, record, update) {
        const handler = new OptEfsHandler()
        const { errors: { BadRequestError } } = fortune
        const { request: { method } } = context
        switch (method) {
            case "create":
                const date = new Date()
                if (!record.created) {
                    record.created = date
                }
                record.id = ObjectUtil.generateId()
                handler.create(record.id)
                return record
        }
    }
}
