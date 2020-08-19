import * as d3 from "d3"
import {CircleCharts} from "../circlecharts"
import {LinearScale} from "../../scale/linear"

export class MaxCircleCharts extends CircleCharts {
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
				domain: [this.source.min()[0] * 0.9, this.source.max()[0]*1.1],
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
				domain: [this.source.min()[1] * 0.9, this.source.max()[1]*1.1],
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
				rangeRound: [16, 140]
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

        const gs = svg.selectAll("g")
                    .data(this.source.apply())
                    .enter()
                    .append("g")

        gs.append("circle")
            .attr("fill", d => {
                return d.EI > 100 ? "url('#EIRadia')" : "url('#defaultEI')"
            })
			.attr("cx", d => xScale(this.source.measure(d)[0]))
			.attr("cy", d => yScale(this.source.measure(d)[1]))
            .attr("r", d => rScale(this.source.measure(d)[2]))
            .attr("clip-path", "url(#chart-area)")
        
        gs.append("text")
            .attr("x", d => {
                const h = xScale(this.source.measure(d)[0])
                const t = d.k.length * 12 / 2
                
                return h - t
            })
            .attr("y", d => yScale(this.source.measure(d)[1]) + 5)
            .text(d => d.k)
            .attr("font-size", "12px")
            .attr("fill", "#6C6F7D")
	}

	/**
	 * 4. interactivity
	 */
	events() {
		console.error("not implemented")
    }
    
}