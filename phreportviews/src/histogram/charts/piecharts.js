import * as d3 from "d3"
import {Charts} from "./chats"

export class PieCharts extends Charts {

	constructor(
		source,
		theme,
		scales = null) {

		super(source, theme, scales)
	}

	render(svg, ivp) {
		const outerRadius = ivp.w / 2
		const innerRadius = 0

		const arc =
			d3.arc()
				.innerRadius(innerRadius)
				.outerRadius(outerRadius)

		const pie = d3.pie().value(d => this.source.measure(d)[1])
		const arcs = svg.selectAll("g.arc")
			.data(pie(this.source.apply()))
			.enter()
			.append("g")
			.attr("class", "arc")
			.attr("transform", "translate(" + outerRadius + ", " + outerRadius + ")")

		arcs.append("path")
			.attr("fill", (d,i) => this.theme.colors(i))
			.attr("d", arc)

		arcs.append("text")
			.attr("transform", d => "translate(" + arc.centroid(d) + ")")
			.attr("text-anchor", "middle")
			// .text(d => this.source.measure(d)[0])
			.text(d => "ab")
	}

	/**
	 * 4. interactivity
	 */
	events() {
		console.error("not implemented")
	}
}
