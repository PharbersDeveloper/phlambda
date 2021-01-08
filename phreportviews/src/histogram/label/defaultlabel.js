
export class label {
	render(svg, source, xs, ys, cns = "text-label") {
		// svg.selectAll("text")
		// 	.data(source.apply())
		// 	.enter()
		// 	.append("text")
		// 	.text((d) => source.measure(d))
		// 	.attr("x", (d, i) => xs(i) + xs.bandwidth() / 2)
		// 	.attr("y", (d) => ys(source.measure(d)) + 14)
		// 	.attr("font-family", "sans-serif")
		// 	.attr("font-size", "11px")
		// 	.attr("fill", "white")
		// 	.attr("text-anchor", "middle")
		// 	.attr("class", cns)
	}
}

export default label
