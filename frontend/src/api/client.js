/**
 * Base HTTP client for talking to the FastAPI backend (app.py).
 *
 * Nothing else in the frontend should call `fetch` directly against
 * the backend — every request goes through here so the base URL,
 * headers, and error shape stay in one place.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * A normalized error thrown for any non-2xx response or network failure.
 * `status` is null for network-level failures (backend unreachable).
 */
export class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  const isFormData = options.body instanceof FormData;

  let response;
  try {
    response = await fetch(url, {
      ...options,
      headers: {
        // Let the browser set its own Content-Type (with boundary) for
        // multipart uploads; default to JSON everywhere else.
        ...(isFormData ? {} : { "Content-Type": "application/json" }),
        ...(options.headers || {}),
      },
    });
  } catch (networkError) {
    throw new ApiError(
      "Could not reach the backend. Is the FastAPI server running?",
      null,
      networkError.message,
    );
  }

  // Attempt to parse JSON regardless of status, since FastAPI error
  // bodies are JSON too (e.g. { "detail": "..." }).
  let body = null;
  const text = await response.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = { detail: text };
    }
  }

  if (!response.ok) {
    const detail = body?.detail || response.statusText || "Request failed.";
    throw new ApiError(detail, response.status, detail);
  }

  return body;
}

export const apiClient = {
  get: (path) => request(path, { method: "GET" }),
  post: (path, data) =>
    request(path, {
      method: "POST",
      body: data !== undefined ? JSON.stringify(data) : undefined,
    }),
  delete: (path) => request(path, { method: "DELETE" }),
  postForm: (path, formData) =>
    request(path, {
      method: "POST",
      body: formData,
    }),
};

export { API_BASE_URL };
