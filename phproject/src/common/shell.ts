
import util from "util"

interface IShell {
    cmd(shell: string): IShell
    exec(): any
}

export default class Shell implements IShell {

    public static get getIns() {
        if (!Shell.ins) {
            Shell.ins = new Shell()
        }
        return Shell.ins
    }
    private static ins: Shell = null
    private shell: string = ""

    private constructor() {}

    public cmd(shell: string) {
        this.shell = shell
        return this
    }

    public async exec() {
        const process = util.promisify(require("child_process").exec)
        if (!this.shell) {
            throw new Error("Shell Is Null")
        }
        return await process(this.shell)
    }
}
