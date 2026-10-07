/**
 * Centralized shape definitions matching app.py's Pydantic models.
 * Plain JS + JSDoc (no TypeScript) so this stays approachable without
 * a separate build step.
 *
 * @typedef {"local" | "web" | "general"} Route
 * @typedef {"ollama" | "gemini" | "openrouter"} Provider
 * @typedef {"document" | "web"} CitationType
 *
 * @typedef {Object} Citation
 * @property {number} id
 * @property {CitationType} type
 * @property {string} source
 * @property {number|null} page
 * @property {number|null} score
 * @property {string|null} url
 * @property {string} [chunk] - Retrieved text chunk (for document citations)
 * @property {Object} [metadata] - Additional metadata
 * @property {number} [metadata.chunkIndex]
 * @property {string} [metadata.embeddingModel]
 * @property {number} [metadata.faissScore]
 * @property {number} [metadata.hybridScore]
 *
 * @typedef {Object} ChatResponse
 * @property {string} answer
 * @property {Route} route
 * @property {Provider} provider
 * @property {string} model
 * @property {Citation[]} citations
 *
 * @typedef {"user" | "assistant"} MessageRole
 *
 * @typedef {Object} ChatMessage
 * @property {string} id
 * @property {MessageRole} role
 * @property {string} content
 * @property {Route} [route]
 * @property {Provider} [provider]
 * @property {string} [model]
 * @property {Citation[]} [citations]
 * @property {boolean} [isError]
 * @property {string} [conversationId]
 * @property {number} [timestamp]
 *
 * @typedef {Object} Conversation
 * @property {string} id
 * @property {string} title
 * @property {ChatMessage[]} messages
 * @property {number} createdAt
 * @property {number} updatedAt
 *
 * @typedef {Object} DocumentEntry
 * @property {string} id
 * @property {string} filename
 * @property {"pdf" | "docx"} type
 * @property {number|null} pages
 * @property {"processed" | "processing" | "failed"} status
 */

export {};
