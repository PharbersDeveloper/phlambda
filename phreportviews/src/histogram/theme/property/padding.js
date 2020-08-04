
export const defaultPaddingValue = 8

export class Padding {
	constructor(v = [defaultPaddingValue, defaultPaddingValue, defaultPaddingValue, defaultPaddingValue]) {
		this.up = v[0]
		this.right = v[1]
		this.bottom = v[2]
		this.left = v[3]
	}
}

export default new Padding()
