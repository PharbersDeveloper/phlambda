
import * as d3 from "d3"
import DefaultAdapter from "../adapter/defaultadapter"

export class MemoryDatasource {
	constructor(dataset, adapter = DefaultAdapter) {
		this.dataset = dataset
		this.adapter = adapter
	}

	apply(key) {
		if (key === undefined) return this.dataset
		else this.dataset.map (x => this.adapter.apply(key, x.key))
	}

	max() {
		return d3.max(this.dataset, d => this.adapter.measure(d))
	}

	min() {
		return d3.min(this.dataset, d => this.adapter.measure(d))
	}

	length() {
		return this.dataset.length
	}
}
