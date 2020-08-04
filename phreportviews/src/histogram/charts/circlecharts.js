import * as d3 from "d3"
import {Charts} from "./chats"
import {LinearScale} from "../scale/linear"

export class CircleCharts extends Charts {

	constructor(
		source,
		theme,
		scales = {
			x: new LinearScale(),
			y: new LinearScale(),
			r: new LinearScale()
		}) {

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

	genRScale(ivp) {
		const r = this.scales["r"]
		if (r) {
			const opt = {
				domain: [0, this.source.max()[2]],
				rangeRound: [1, 3]
			}
			return r.genScale(opt)
		} else {
			return d3.scaleLinear()
				.domain([0, this.source.max()[1]])
				.range([ivp.h, ivp.y])
		}
	}

	render(svg, ivp) {
		const xScale = this.genXScale(ivp)
		const yScale = this.genYScale(ivp)
		const rScale = this.genRScale(ivp)

		svg.selectAll("circle")
			.data(this.source.apply())
			.enter()
			.append("circle")
			.attr("cx", d => xScale(this.source.measure(d)[0]))
			.attr("cy", d => yScale(this.source.measure(d)[1]))
			.attr("r", d => rScale(this.source.measure(d)[2]))
			.attr("fill", (d, i) => this.theme.colors(i))
	}

	/**
	 * 4. interactivity
	 */
	events() {
		console.error("not implemented")
	}
}
