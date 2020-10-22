export declare class Adapter {
    private static instance;
    private adapterMapping;
    constructor();
    static get init(): Adapter;
    getAdapter(name: string): any;
}
