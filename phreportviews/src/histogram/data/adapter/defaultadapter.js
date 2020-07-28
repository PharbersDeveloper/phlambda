
export class MeasureArrayAdapter {
    constructor() {
        this.mk = ""
    }

    apply(m, k, v) {
        return v
    }

    measure(d) {
        return d
    }
}

export default new MeasureArrayAdapter()
