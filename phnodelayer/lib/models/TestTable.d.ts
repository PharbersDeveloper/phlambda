declare class TestTable {
    model: any;
    operations: {
        hooks: {
            event: ((context: any, record: any, update: any) => any)[];
        };
    };
    protected hooksDate(context: any, record: any, update: any): any;
}
export default TestTable;
