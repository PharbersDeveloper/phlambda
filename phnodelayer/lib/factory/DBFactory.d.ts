export default class DBFactory {
    private static instance;
    private typeAnalyzerMapping;
    private serverConf;
    constructor();
    static get getInstance(): DBFactory;
    getStore(name?: string): any;
    private buildStore;
}
