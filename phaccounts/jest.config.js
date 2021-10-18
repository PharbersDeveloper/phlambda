module.exports = {
    reporters: [
        'default',
        [ 'jest-junit', {
            outputDirectory: './phauth-report-directory',
            outputName: 'phauth-report-file.xml',
        } ]
    ]
};