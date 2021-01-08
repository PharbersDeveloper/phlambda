import * as d3 from "d3"
import {Charts} from "./chats"
import {LinearScale} from "../scale/linear"

export class LineCharts extends Charts {

	constructor(
		source,
		theme,
		scales = { x: new LinearScale(), y: new LinearScale() }) {

		super(source, theme, scales)
	}

	genXScale(ivp) {
		const x = this.scales["x"]
		if (x) {
			const opt = {
				domain: [0, this.source.max()[0]],
				rangeRound: [ivp.x, ivp.w],
				paddingInner: 0.05
			}
			return x.genScale(opt)
		} else {
			return d3.scaleBand()
				.domain([0, this.source.max()[0]])
				.rangeRound([ivp.x, ivp.w])
				.paddingInner(0.05)
		}
	}

	genYScale(ivp) {
		const y = this.scales["y"]
		if (y) {
			const opt = {
				domain: [0, this.source.max()[1]],
				rangeRound: [ivp.h, ivp.y]
			}
			return y.genScale(opt)
		} else {
			return d3.scaleLinear()
				.domain([0, this.source.max()[1]])
				.range([ivp.h, ivp.y])
		}
	}

	render(svg, ivp) {
		const xScale = this.genXScale(ivp)
		const yScale = this.genYScale(ivp)

		//Define line generator
		const line = d3.line()
			.x(d => xScale(this.source.measure(d)[0]))
			.y(d => yScale(this.source.measure(d)[1]))

		svg.append("path")
			.datum(this.source.apply())
			.attr("class", "line")
			.attr("d", line)
	}

	/**
	 * 4. interactivity
	 */
	events() {
		console.error("not implemented")
	}
}
