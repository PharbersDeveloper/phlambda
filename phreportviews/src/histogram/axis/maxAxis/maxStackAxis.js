import * as d3 from "d3"
import {Axis} from "../axis";

export const AxisDirections= {
	Left: 'Left',
	Right: 'Right',
	Up: 'Up',
	Bottom: 'Bottom'
}

export const defaultAxisWidth = 25

export class MaxStackAxis extends Axis{
	constructor(direction = AxisDirections.Bottom, width = defaultAxisWidth) {
        super(direction, width)

		this.direction = direction
        this.width = defaultAxisWidth
        
        this.type = "stack"
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

        for(let j = 0; i + j * step < a; j++) {
            arr.push(i + j * step)
        }

        arr.push(a)
        this.ticksArr =  arr
    }
    

	render(svg, s, ivp) {
        const f = d3.format(".3s")
        const a = this.ticksArr
        const timeArr = ["2018-01", "2019-01",]
        const timeF = d3.timeFormat("%Y-%m");
        if (this.isBottom()) {
			const xAxis = d3.axisBottom().scale(s).tickValues(timeArr.map(it => { return new Date(it) })).tickFormat(timeF)
			svg.append("g")
                .attr("transform", "translate(0," + ivp.h + ")")
                .attr("class", "stack-axis-x")
				.call(xAxis)
		} else if (this.isLeft()) {
			const yAxis = d3.axisLeft().scale(s).tickValues(a).tickFormat(function(d) { return f(d).replace('M', '(Mn)'); } )
			svg.append("g")
                .attr("transform", "translate(" + (ivp.x - 30) + ", 0)")
                .attr("class", "stack-axis-y")
				.call(yAxis)
        }
    }

    renderBackgroundLine(svg, ys, ivp) {
        const a = this.ticksArr
        svg.selectAll(".hline")
            .data(a)
            .enter()
            .append("line")
            .attr("x1", ivp.x)
            .attr("y1", function(d) {
                return ys(d)
            })
            .attr("x2", ivp.x + ivp.w)
            .attr("y2", d => ys(d))
            .attr("stroke", "#EBECF0")
            .attr("stroke-dasharray", "3,3")
    }

    renderExtraXAxis(svg, ivp) {
        svg.append("line")
            .attr("stroke", "#848996")
            .attr("x1", ivp.x - 32)
            .attr("y1", ivp.h)
            .attr("x2", ivp.x + ivp.w - 32)
            .attr("y2", ivp.h)
            .attr("height", 1)
    }

    showXTitle(svg, xTitle, ivpInfo) {
        if (xTitle) {
            svg.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(${ivpInfo.bottom.w/2}, ${ivpInfo.bottom.h/2})`)
                .text(xTitle)
		}
    }

    showYTitle(svg, yTitle, ivpInfo) {
        if (yTitle) {
            svg.append("text")
                .attr("font-size", "12px")
                .attr("fill", "#848996")
                .attr("transform", `translate(${ivpInfo.left.x + ivpInfo.left.w / 2 }, ${ivpInfo.left.y + ivpInfo.left.h / 2 - 20}) rotate(270, 10 10)`)
                .text(yTitle)
		}
    }
}
