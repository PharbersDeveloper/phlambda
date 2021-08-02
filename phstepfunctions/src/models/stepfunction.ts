
class StepFunction {
    model: any = {
        function: {
            name: String,
            type: String,
            created: Number,
            tags: Object,
        }
    }

    operations = {
        hooks: {}
    }
}

export default StepFunction
