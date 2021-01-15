import {MemoryDatasource} from "../source/memdatasource"
import * as d3 from "d3"
import {Datasource} from "../source/datasource"

export class MeasureArrayAdapter extends Datasource {
    constructor(ds) {
        super()
        this.ds = ds
    }

    apply(key) {
        return this.ds.apply(key)
    }

    max() {
        return d3.max(this.ds.dataset, d => d)
    }

    min() {
        return d3.min(this.ds.dataset, d => d)
    }

    length() {
        return this.ds.dataset.length
    }

    measure(d) {
        return this.ds.measure(d)
    }
}

export default new MeasureArrayAdapter()