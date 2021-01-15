
import * as d3 from "d3"
import {Scale} from "./scale"

export class BandScale extends Scale {

	genScale(opt) {
		const dm = opt["domain"]
		const rg = opt["rangeRound"]
		const pi = opt["paddingInner"]
		return d3.scaleBand()
			.domain(dm)
			.rangeRound(rg)
			.paddingInner(pi)
	}
}