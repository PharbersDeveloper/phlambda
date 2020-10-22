"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class TestTable {
    constructor() {
        this.model = {
            event: {
                name: String,
                time: Date,
            },
        };
        this.operations = {
            hooks: {
                event: [this.hooksDate],
            },
        };
    }
    hooksDate(context, record, update) {
        const { request: { method, meta: { language }, }, } = context;
        switch (method) {
            case 'create':
                record.time = new Date();
                return record;
        }
    }
}
exports.default = TestTable;
