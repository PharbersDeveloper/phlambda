
import * as d3 from "d3"
import {Datasource} from "./datasource"

export class MemoryDatasource extends Datasource {
	constructor(dataset) {
		super()
		this.dataset = dataset
	}

	apply(key) {
		if (key === undefined) return this.dataset
		else this.dataset.map (x => this.adapter.apply(key, x.key))
	}

	max() {
		return d3.max(this.dataset, d => d)
	}

	min() {
		return d3.min(this.dataset, d => d)
	}

	length() {
		return this.dataset.length
	}

	measure(d) {
		return d
	}
}
