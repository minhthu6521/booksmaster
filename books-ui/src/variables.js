const backend_url = process.env.BACKEND_API || "http://localhost:8002",
    content_api = process.env.CONTENT_API || "http://localhost:8001";

exports.backend_url = backend_url;
exports.content_api = content_api;