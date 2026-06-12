# Security Policy

## Security Controls
- **Input Validation**: Strict file extension and size validation (max 25MB). Uploaded file names are sanitized using `secure_filename`.
- **Credential Protection**: Passwords hashed with bcrypt. JWT tokens signed with HS256 secret keys.
- **Untrusted Content Isolation**: Document content is treated as untrusted text. Retrieved passages are injected strictly into user prompt context, not system instruction prompts.
- **Local Inference Isolation**: Inference runs locally through Ollama, preventing third-party data egress.
- **Ephemeral Storage & Deletion**: Deleting a document removes its physical file, database records, and vector embeddings in Qdrant.
