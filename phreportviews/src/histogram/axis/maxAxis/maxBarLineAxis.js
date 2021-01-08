import * as d3 from "d3"
import {Axis} from "../axis";

export const AxisDirections= {
	Left: 'Left',
	Right: 'Right',
	Up: 'Up',
	Bottom: 'Bottom'
}

export const defaultAxisWidth = 25

export class MaxBarLineAxis extends Axis{
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
        const leftYFormat = d3.format(".3s")
        const rightYFormat = d3.format(".0%")
        const timeF = d3.timeFormat("%Y-%m");
        const leftYArr = this.ticksArr
        const timeArr = ["2018-01", "2019-01",]
        if (this.isBottom()) {
			const xAxis = d3.axisBottom().scale(s).tickValues(timeArr.map(it => { return new Date(it) })).tickFormat(timeF)
			svg.append("g")
                .attr("transform", `translate(0,${ivp.h})`)
                .attr("class", "stack-axis-x")
				.call(xAxis)
		} else if (this.isLeft()) {
			const yAxis = d3.axisLeft().scale(s).tickValues(leftYArr).tickFormat(function(d) { return leftYFormat(d).replace('M', '(Mn)'); } )
			svg.append("g")
                .attr("transform", "translate(" + (ivp.x - 30) + ", 0)")
                .attr("class", "stack-axis-y")
				.call(yAxis)
        } else if (this.isRight()) {
            
            const percentArr = [-1, -0.5, 0.0, 0.5, 1]
            const yAxis = d3.axisRight().scale(s).tickValues(percentArr).tickFormat(rightYFormat)
			svg.append("g")
                .attr("transform", "translate(" + (ivp.x - 80 + ivp.w) + ", 0)")
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
            .attr("x2", ivp.x + ivp.w - 80)
            .attr("y2", d => ys(d))
            .attr("stroke", "#EBECF0")
            .attr("stroke-dasharray", "3,3")
    }

    renderExtraXAxis(svg, ys,ivp) {
        svg.append("line")
            .attr("stroke", "#848996")
            .attr("x1", ivp.x - 32)
            .attr("y1", ivp.h)
            .attr("x2", ivp.x + ivp.w - 80)
            .attr("y2", ivp.h)
            .attr("height", 1)
    }

    showLeftTitle(svg, title, ivpinfo) {
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpinfo.left.x + ivpinfo.left.w/3}, ${ivpinfo.left.y + ivpinfo.left.h/2 - 18})  rotate(270, 10 10)`)
            .text(title)
    }

    showRightTitle(svg, title, ivpinfo) {
        svg.append("text")
            .attr("font-size", "12px")
            .attr("fill", "#848996")
            .attr("transform", `translate(${ivpinfo.right.x}, ${ivpinfo.right.y + ivpinfo.right.h/2 - 18}) rotate(270, 10 10)`)
            .text(title)
		
    }

}
