import IStrategy from "../common/IStrategy"

export default class LogContext {
    private strategy: IStrategy
    private readonly events: any[]
    constructor(events: any[]) {
        this.events = events
    }

    setStrategy(strategy: IStrategy) {
        this.strategy = strategy
    }

    async execute() {
        return await this.strategy.extractLog(this.events)
    }
}
