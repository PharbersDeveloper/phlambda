exports.handler = function iterator (event, context, callback) {
    let index = event.iterator.index
    let step = event.iterator.step
    let count = event.iterator.count

    index += step

    callback(null, {
        index,
        step,
        count,
        continue: index < count
    })
}