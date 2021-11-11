class Index {
    model: any = {
        stateMachine: {
            type: String, // 分为AirFlow或Step Function
            // arn: String,
            name: String, // 如果是AirFLow name = DAGName|StepFunction name = arn
            project: String, // 外链project id
            displayName: String,
            // version: String,
        },
        project: {
            provider: String,
            name: String,
            owner: String,
            type: String, // saas 无 Flow  pass有Flow
            created: Date,
        }
    }

    operations = {
        hooks: {}
    }
}

export default Index
