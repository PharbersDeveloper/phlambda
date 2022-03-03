import { execSync } from "child_process"
import * as fs from "fs"

export default class OptEfsHandler {
    private paths: string[] = [
        "/airflow",
        "/tmp",
        "/worksapce",
        "/clickhouse"
    ]
    private mountPath = process.env.MOUNTPATH

    private existsPath(path) {
        return fs.existsSync(path)
    }

    private createPath(path) {
        return execSync(`mkdir -p ${path}`)
    }

    private copyPath(source, targetPath) {
        return execSync(`cp -r ${source} ${targetPath}`)
    }

    private chmodPath(path) {
        return execSync(`chmod -R 777 ${path}`)
    }

    private removePath(path) {
        return execSync(`rm -rf ${path}`)
    }

    create(projectId) {
        const projectPath = this.mountPath + projectId + "/"
        this.paths.forEach((path) => {
            const completePath = projectPath + path
            const result = this.existsPath(completePath)
            if (!result) {
                this.createPath(completePath)
            }
        })

        this.copyPath(this.mountPath + "airflow/", projectPath)
        this.chmodPath(projectPath)
    }

    remove(projectId) {
        const projectPath = this.mountPath + projectId + "/"
        this.removePath(projectPath)
    }
}
