import * as d3 from "d3"

export const AxisDirections= {
	Left: 'Left',
	Right: 'Right',
	Up: 'Up',
	Bottom: 'Bottom'
}

export const defaultAxisWidth = 25

export class Axis {
	constructor(direction = AxisDirections.Bottom, width = defaultAxisWidth) {
		this.direction = direction
		this.width = defaultAxisWidth
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

	render(svg, s, ivp) {
		if (this.isBottom()) {
			const xAxis = d3.axisBottom().scale(s)
			svg.append("g")
				.attr("class", "axis")
				.attr("transform", "translate(0," + ivp.h + ")")
				.call(xAxis)
		} else if (this.isLeft()) {
			const yAxis = d3.axisLeft().scale(s)
			svg.append("g")
				.attr("class", "axis")
				.attr("transform", "translate(" + ivp.x + ", 0)")
				.call(yAxis)
		}
	}
}
