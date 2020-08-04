
import * as d3 from "d3"
import {Scale} from "./scale"

export class LinearScale extends Scale {

	genScale(opt) {
		const dm = opt["domain"]
		const rg = opt["rangeRound"]
		return d3.scaleLinear()
			.domain(dm)
			.range(rg)
	}
}
