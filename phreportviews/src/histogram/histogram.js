
export class Histogram {
    constructor(
        source,
        theme,
        scales) {

        this.theme = theme
        this.source = source
        this.scales = scales
    }

    displayHistogram(width, height) {
        this.render(width, height)
        // this.events()
    }

    /**
     * 3. Render the initial view
     */
    render(width, height) {
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
