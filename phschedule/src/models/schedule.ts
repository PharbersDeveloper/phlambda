
const records = {
    // test Fix Bug PBDP-401: add fileIndex for the upload files'
    // TODO: will gen another bug for the new version & is new version
    fileIndex: {
        fileName: String,
        owner: String,
        martTags: Array(String),
        providers: Array(String),
        markets: Array(String),
        molecules: Array(String),
        dataCover: Array(String),
        geoCover: Array(String),
        labels: Array(String),
        url: String,
        createdTime: Date,
        size: Number,
        extension: String,
        assets: { link: "asset", isArray: true, inverse: "fi" }
    },
    file: {
        fileName: String,
        sheetName: String,
        startRow: Number,
        label: String,
        extension: String,
        size: Number,
        url: String,
        assetFile: { link: "asset", inverse: "file" }
    },
    job: {
        codeProvider: String,
        codeRepository: String,
        codeBranch: String,
        codeVersion: String,
        jobContainerId: String,
        create: Date,
        description: String,
        gen: { link: "dataSet", inverse: "job" }
    },
    dbSource: {
        dbType: String,
        url: String,
        user: String,
        pwd: String,
        dbName: String,
        create: Date,
        assetDbs: { link: "asset", inverse: "dbs" }
    },
    dataSet: {
        colNames: Array(String),
        length: Number,
        url: String,
        description: String,
        tabName: String,
        status: String,
        parent: { link: "dataSet", isArray: true, inverse: "child" },
        child: { link: "dataSet", isArray: true, inverse: "parent" },
        job: { link: "job", inverse: "gen" },
        mart: { link: "mart", inverse: "dfs" },
        assetDs: { link: "asset", inverse: "dfs" }
    },
    mart: {
        dfs: { link: "dataSet", isArray: true, inverse: "mart" },
        name: String,
        url: String,
        dataType: String,
        description: String,
        assetMart: { link: "asset", inverse: "mart" }
    },
    asset: {
        name: String,
        description: String,
        owner: String,
        accessibility: String,
        version: String,
        isNewVersion: Boolean,
        dataType: String, // candidate: database, file, stream, application, mart, cube
        fi: { link: "fileIndex", inverse: "assets" },
        file: { link: "file", inverse: "assetFile" },
        dbs: { link: "dbSource", inverse: "assetDbs" },
        dfs: { link: "dataSet", isArray: true, inverse: "assetDs" },
        mart: { link: "mart", inverse: "assetMart" },
        martTags: Array(String),
        providers: Array(String),
        markets: Array(String),
        molecules: Array(String),
        dataCover: Array(String),
        geoCover: Array(String),
        labels: Array(String),
        createTime: Date
    }
}

export default records
