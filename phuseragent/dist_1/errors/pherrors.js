"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.errors2response = exports.PhInvalidClient = exports.PhInvalidParameters = void 0;
exports.PhInvalidParameters = {
    status: 501,
    code: -3,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: JSON.stringify({ message: "Invalid Parameters" }),
};
exports.PhInvalidClient = {
    status: 403,
    code: -4,
    headers: { "Content-Type": "application/json", "Accept": "application/json" },
    message: JSON.stringify({ message: "Invalid Client, Please Contact Pharbers" }),
};
function errors2response(err, response) {
    response.statusCode = err.status;
    // @ts-ignore
    response.headers = err.headers;
    // @ts-ignore
    response.body = err.message;
}
exports.errors2response = errors2response;
//# sourceMappingURL=pherrors.js.map