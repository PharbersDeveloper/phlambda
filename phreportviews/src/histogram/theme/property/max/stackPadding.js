import {Padding } from "../padding"

export const defaultPaddingValue = 8

export class StackPadding extends Padding  {
	constructor(v = [defaultPaddingValue, 32, defaultPaddingValue, 32]) {
        super()
        
		this.up = v[0]
		this.right = v[1]
		this.bottom = v[2]
		this.left = v[3]
	}
}

export default new StackPadding()
