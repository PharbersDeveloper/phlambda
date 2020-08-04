import {label} from "./defaultlabel"

export class PieLabel extends label {
	render(arcs, arc, source,  cns = "pie-label") {
		arcs.append("text")
			.attr("transform", d => "translate(" + arc.centroid(d) + ")")
			.attr("text-anchor", "middle")
			.attr("class", cns)
			.text(d => source.measure(d.data)[0])
	}
}

export default new PieLabel()
