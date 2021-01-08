'use strict';

describe('Test report index', function () {
	it('verify find view', async () => {

		const express = require('express')
		const app = express()

		const fs = require('fs')
		const Handlebars = require("handlebars")
		const exStatic = require("express-static")
		app.use('/style', exStatic('./style'))
		app.use('/dist', exStatic('./dist'))
		const content = fs.readFileSync("/Users/simon/Desktop/pharbersBitBucket/phlambda/phreportviews/template/max/bubble.hbs")
		const template = Handlebars.compile(content.toString())
		const histogram = template({
			histogramId: "test",
			histogramPieId: "pietest",
			name:"simon",
			width: 1052,
			height: 360,
			xTitle: "产品市场份额",
			yTitle: "市场增长率(%)"
		})

		app.get('/', function (req, res) {
			res.send(histogram)
		})

		app.listen(3000)

	}).timeout(30 * 60 * 60 * 1000)
});
