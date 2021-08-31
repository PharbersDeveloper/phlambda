
export default abstract class Config {
    protected typeAnalyzerMap: Map<string, any> = new Map()

    abstract getConf(key: string): Map<string, any>
}
