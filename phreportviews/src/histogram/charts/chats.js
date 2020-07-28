import * as d3 from "d3"

export class Charts {

	constructor(
		source,
		theme) {

		this.source = source
		this.theme = theme
	}

	genXScale(ivp) {
		return d3.scaleBand()
			.domain(d3.range(this.source.length()))
			.rangeRound([ivp.x, ivp.w])
			.paddingInner(0.05)
	}

	genYScale(ivp) {
		return d3.scaleLinear()
			.domain([0, this.source.max()])
			.range([ivp.h, ivp.y])
	}

	render(svg, ivp) {
		console.error("not implemented")
		throw new Error("not Implemented")
	}

	/**
	 * 4. interactivity
	 */
	events() {
		console.error("not implemented")
		throw new Error("not Implemented")
	}
}
