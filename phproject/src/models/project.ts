import * as fortune from "fortune"
import { Http } from "../common/http"

class Project {
    public model: any = {
        project: {
            name: String,
            owner: String,
            created: Date,
            modified: Date,
            description: String,
        },
        trigger: {
            dagId: String,
            timeLeft: String,
            timeRight: String,
            molecule: String,
            project: String,
            atc: String,
            outSuffix: String,
            email: String,
            version: String,
            status: String,
        }
    }

    public operations = {
        hooks: {
            project: [ this.hooksDate ],
            trigger: [ this.hooksDate ]
        }
    }

    protected async hooksDate(context, record, update) {
        const { request: { method, type, meta: { language } } } = context
        const { errors: { BadRequestError } } = fortune
        switch (method) {
            case "create":
                if (type === "trigger") {
                    const airflowRunDagUrl = `http://192.168.62.76:30086/api/v1/dags/${record.dagId}/dagRuns`
                    const parm = {}
                    for (const item of Object.keys(record)) {
                        const key = item.replace(/([A-Z])/g, "_$1").toLowerCase()
                        if (record[item] !== null && record[item] !== undefined) {
                            parm[key] = record[item]
                        }
                    }
                    const res =  await new Http().post(airflowRunDagUrl, {conf: parm})
                    if (res.status !== 200) { throw new BadRequestError(res.statusText) }
                    record.status = res.statusText
                } else {
                    const date = new Date()
                    if (!record.created) {
                        record.created = date
                    }
                    record.modified = date
                }
                return record
            case "update":
                if (type !== "trigger") {
                    update.replace.modified = new Date()
                }
                return update
        }
    }
}

export default Project
