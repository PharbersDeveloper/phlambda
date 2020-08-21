import * as d3 from "d3"
import {Axis} from "../axis";

export const AxisDirections= {
	Left: 'Left',
	Right: 'Right',
	Up: 'Up',
	Bottom: 'Bottom'
}

export const defaultAxisWidth = 25

export class MaxMapAxis extends Axis{
	constructor(direction = AxisDirections.Bottom, width = defaultAxisWidth) {
        super(direction, width)

		this.direction = direction
        this.width = defaultAxisWidth
        
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

}
