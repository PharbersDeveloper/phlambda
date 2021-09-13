import { IStore, Register, StoreEnum } from "phnodelayer"

class Max {
    model: any = {
        project: {
            provider: String,
            time: Number,
            actions: String,
            mapper: String,
        },
        jobLog: {
            provider: String,
            owner: String,
            showName: String,
            time: Number,
            version: String,
            code: Number,
            jobDesc: String,
            jobCat: String,
            comments: String,
            message: String,
            date: Number
        }
    }

    operations = {
        hooks: {
            jobLog: [this.hookProjectInput]
        }
    }

    async hookProjectInput(context, record, update) {
        const { request: { method } } = context
        function clone(obj) {
            const cloneObj = {}
            for (const item of Object.keys(obj)) {
                cloneObj[item] = record[item]
            }
            delete cloneObj["id"]
            delete cloneObj["provider"]
            delete cloneObj["time"]
            return cloneObj
        }
        async function JobLogCreate() {
            let createProject = await context.transaction.
                find("project", null, { match: { provider: record.provider, time: record.time} })
            const cloneRecord = clone(record)
            if (createProject.length === 0) {
                createProject = await context.transaction.create("project", {
                    provider: record.provider,
                    time: record.time,
                    actions: "[]"
                })
            }
            const actions = JSON.parse(createProject[0].actions)
                .filter((item) => item.jobCat !== record.jobCat)
            actions.push(cloneRecord)
            const updateProject = {
                id: createProject[0].id,
                replace: {
                    actions: JSON.stringify(actions)
                }
            }
            await context.transaction.update("project", [updateProject])
        }
        async function JobLogUpdate() {
            let resultProject = await context.transaction.
                find("project", null, { match: { provider: record.provider, time: record.time} })
            const cloneRecord = clone(record)
            for (const item of Object.keys(update.replace)) {
                cloneRecord[item] = update.replace[item]
            }
            const actions = JSON.parse(resultProject.payload.records[0].actions)
                .filter((item) => item.jobCat !== record.jobCat)
            actions.push(cloneRecord)
            const updateProject = [{
                id: resultProject.payload.records[0].id,
                replace: {
                    actions: JSON.stringify(actions)
                }
            }]
            await context.transaction.update("project", updateProject)
        }
        switch (method) {
            case "create":
                await JobLogCreate()
                return record
            case "update":
                await JobLogUpdate()
                return update
        }
    }
}

export default Max
