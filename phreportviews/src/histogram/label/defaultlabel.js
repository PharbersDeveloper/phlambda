
import * as d3 from "d3"

export class label {
	render(svg, source, xs, ys, cns = "text-label") {
		svg.selectAll("text")
			.data(source.apply())
			.enter()
			.append("text")
			.text((d) => d.toString())
			.attr("x", (d, i) => xs(i) + xs.bandwidth() / 2)
			.attr("y", (d) => ys(d) + 14)
			.attr("font-family", "sans-serif")
			.attr("font-size", "11px")
			.attr("fill", "white")
			.attr("text-anchor", "middle")
			.attr("class", "text-label")
	}
}

export default new label()
