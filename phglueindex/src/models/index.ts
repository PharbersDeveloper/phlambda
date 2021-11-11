class Index {
    model: any = {
        db: {
            name: String,
            provider: String,
            tables: { link: "table", isArray: true, inverse: "db" },
        },
        table: {
            name: String,
            database: String,
            provider: String,
            version: String,
            db: { link: "db", inverse: "tables" },
        }
    }

    operations = {
        hooks: {}
    }
}

export default Index
