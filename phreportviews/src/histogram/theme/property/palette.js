
import * as d3 from "d3"

export class Palette {
    constructor(cns = []) {
        if (cns.length > 0) {
            this.colors = d3.scaleOrdinal(cns)
        } else {
            this.colors = d3.scaleOrdinal(d3.schemeCategory10)
        }
    }
}

export default new Palette()
