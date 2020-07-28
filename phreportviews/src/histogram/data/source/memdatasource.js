
import { DefaultAdapter } from "../adapter/defaultadapter"

export class MemoryDatasource {
	constructor(dataset, adapter = DefaultAdapter) {
		this.dataset = dataset
		this.adapter = adapter
	}

	apply(key) {
		if (key === undefined) return this.dataset
		else this.dataset.map (x => this.adapter.apply(key, x.key))
	}
}
