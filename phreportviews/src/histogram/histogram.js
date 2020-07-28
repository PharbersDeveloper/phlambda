
export class Histogram {
    constructor(
        source,
        theme) {

        this.theme = theme
        this.source = source
    }

    displayHistogram(width, height) {
        const dataset = this.source.apply()
        this.render(width, height, dataset)
        // this.events()
    }

    /**
     * 3. Render the initial view
     */
    render(width, height, dataset) {
        console.info("render the view")
        throw new Error("not Implemented")
    }

    /**
     * 4. interactivity
     */
    events() {
        console.error("not implemented")
        throw new Error("not Implemented")
    }
}
