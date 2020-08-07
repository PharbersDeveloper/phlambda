import * as d3 from "d3"
import {Axis} from "../axis";

export const AxisDirections= {
	Left: 'Left',
	Right: 'Right',
	Up: 'Up',
	Bottom: 'Bottom'
}

export const defaultAxisWidth = 25

export class MaxAxis extends Axis{
	constructor(direction = AxisDirections.Bottom, width = defaultAxisWidth) {
        super(direction, width)

		this.direction = direction
        this.width = defaultAxisWidth
        
        this.type = "bubble"
        this.ticksArr = [1,2,3]
	}

	isLeft() {
		return this.direction === AxisDirections.Left
	}

	isRight() {
		return this.direction === AxisDirections.Right
	}

	isUp() {
		return this.direction === AxisDirections.Up
	}

	isBottom() {
		return this.direction === AxisDirections.Bottom
	}

	isX() {
		return this.isUp() || this.isBottom()
	}

	isY() {
		return this.isLeft() || this.isRight()
	}

	axisWidth() {
		return this.width
    }
    
    getAxisTicks(min, max, n) {
        const a = max
        const i = min
        const step = (a-i)/n
        let arr = []

        console.log("?", a, i, step)
        for(let j = 0; i + j * step < a; j++) {
            arr.push(i + j * step)
        }

        arr.push(a)
        this.ticksArr =  arr
    }

	render(svg, s, ivp) {
        this.bubbleRender(svg, s, ivp)
		// if (this.isBottom()) {
		// 	const xAxis = d3.axisBottom().scale(s)//.tickValues([0, "b", "c", "d", "e"])
		// 	svg.append("g")
		// 		.attr("class", "axis")
		// 		.attr("transform", "translate(0," + ivp.h + ")")
		// 		.call(xAxis)
		// } else if (this.isLeft()) {
		// 	const yAxis = d3.axisLeft().scale(s)
		// 	svg.append("g")
		// 		.attr("class", "axis")
		// 		.attr("transform", "translate(" + ivp.x + ", 0)")
		// 		.call(yAxis)
		// }
    }

    bubbleRender(svg, s, ivp) {
        // get ticks arr
        const f = d3.format(".0%")
        const a = this.ticksArr
        if (this.isBottom()) {
			const xAxis = d3.axisBottom().scale(s).tickValues(a).tickFormat(f)
			svg.append("g")
				.attr("class", "bubble-axis")
				.attr("transform", "translate(0," + ivp.h + ")")
				.call(xAxis)
		} else if (this.isLeft()) {
			const yAxis = d3.axisLeft().scale(s).ticks(20)
			svg.append("g")
				.attr("class", "bubble-axis")
				.attr("transform", "translate(" + ivp.x + ", 0)")
				.call(yAxis)
        }
        
        
    }

    showXTitle(svg, xTitle, ivp) {
        if (xTitle) {
            svg.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(${ivp.w/2}, ${ivp.h + 40})`)
                .text(xTitle)
		}
    }

    showYTitle(svg, yTitle, ivp) {
        if (yTitle) {
            svg.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(40, ${ivp.h / 2}) rotate(270, 10 10)`)
                .text(yTitle)
		}
    }

    renderBackgroundLine(svg, ivp) {
        // ivp {x: 73, y: 8, w: 1136, h: 379}
        const h = [80,190]
        const v = [228, 456, 684, 912]

        svg.selectAll(".hline")
            .data(h)
            .enter()
            .append("line")
            .attr("x1", ivp.y + ivp.x)
            .attr("y1", d => ivp.x + d)
            .attr("x2", ivp.y + ivp.w)
            .attr("y2", d => ivp.x + d)
            .attr("stroke", "#EBECF0")
            .attr("stroke-dasharray", "3,3")

        svg.selectAll(".vline")
            .data(v)
            .enter()
            .append("line")
            .attr("x1", d => ivp.x + d)
            .attr("y1", ivp.x)
            .attr("x2", d => ivp.x + d)
            .attr("y2", ivp.h)
            .attr("stroke", "#EBECF0")
            .attr("stroke-dasharray", "3,3")
    }

    clipChart(svg, ivp) {
         // 裁剪超过坐标轴的图形
         svg.append("clipPath")
            .attr("id", "chart-area")
            .append("rect")
            .attr("x", ivp.x)
            .attr("y", ivp.y)
            .attr("width", 1052)
            .attr("height", 370);
    }
}
