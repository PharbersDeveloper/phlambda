import {IStore} from "phnodelayer"

export default class MaxLogHandler {
    private readonly store: IStore

    constructor(store: IStore) {
        this.store = store
    }

    async exec(event: any) {
        for ( const item of event.Records ) {
            const subject = item?.Sns?.Subject || undefined
            const message = item?.Sns?.Message || undefined
            const attributes = item?.Sns?.MessageAttributes || undefined
            if (message && attributes && subject === "maxlog") {
                await this.syncActionLog(JSON.parse(message), attributes.action.Value)
            }
        }
    }

    private async syncActionLog(content: any, action: string) {
        switch (action) {
            case "update":
                const {
                    logId, provider, owner,
                    showName, time, version,
                    code, jobDesc, jobCat,
                    comments, message, date
                } = content
                const project = await this.store.find("project", null, { match: { provider, time }})
                const actions = JSON.parse(project.payload.records[0].actions).filter((item) => item.jobCat !== jobCat)
                actions.push({
                    owner, showName, version,
                    code, jobDesc, jobCat,
                    comments, message, date
                })
                const updateProjectRecord = {
                    id: project.payload.records[0].id,
                    replace: {actions: JSON.stringify(actions)}
                }
                const updateJobLogRecord = {
                    id: logId,
                    replace: {
                        provider, owner, showName,
                        time, version, code,
                        jobDesc, jobCat, comments,
                        message, date
                    }
                }
                await this.store.update("jobLog", updateJobLogRecord)
                await this.store.update("project", updateProjectRecord)
                break
        }
    }

}
