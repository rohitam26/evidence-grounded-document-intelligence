import uuid
from typing import List, Dict, Any
from app.ingestion.parser import ParsedBlock
from app.utils.hashing import compute_sha256
from app.config import settings

class DocumentChunk:
    def __init__(
        self,
        document_id: str,
        document_name: str,
        page_number: int,
        chunk_index: int,
        section_heading: str,
        content: str,
        source_type: str,
        embedding_model: str = settings.EMBEDDING_MODEL
    ):
        self.chunk_id = str(uuid.uuid4())
        self.document_id = document_id
        self.document_name = document_name
        self.page_number = page_number
        self.chunk_index = chunk_index
        self.section_heading = section_heading
        self.content = content
        self.source_type = source_type
        self.content_hash = compute_sha256(content)
        self.embedding_model = embedding_model

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "document_name": self.document_name,
            "page_number": self.page_number,
            "chunk_index": self.chunk_index,
            "section_heading": self.section_heading,
            "content": self.content,
            "source_type": self.source_type,
            "content_hash": self.content_hash,
            "embedding_model": self.embedding_model
        }

class StructureAwareChunker:
    """Structure-aware chunker that preserves headings, tables, and page numbers."""

    def __init__(self, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(
        self,
        blocks: List[ParsedBlock],
        document_id: str,
        document_name: str
    ) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        chunk_index = 0

        # Group blocks by page and heading to preserve context
        for block in blocks:
            # Tables are self-contained chunks to preserve tabular integrity
            if block.block_type == "table":
                chunks.append(DocumentChunk(
                    document_id=document_id,
                    document_name=document_name,
                    page_number=block.page_number,
                    chunk_index=chunk_index,
                    section_heading=block.heading or "Table Section",
                    content=block.text,
                    source_type="table"
                ))
                chunk_index += 1
                continue

            words = block.text.split()
            if len(words) <= self.chunk_size:
                chunks.append(DocumentChunk(
                    document_id=document_id,
                    document_name=document_name,
                    page_number=block.page_number,
                    chunk_index=chunk_index,
                    section_heading=block.heading,
                    content=block.text,
                    source_type=block.block_type
                ))
                chunk_index += 1
            else:
                # Sliding window chunking with overlap
                start = 0
                while start < len(words):
                    end = min(start + self.chunk_size, len(words))
                    chunk_text = " ".join(words[start:end])
                    chunks.append(DocumentChunk(
                        document_id=document_id,
                        document_name=document_name,
                        page_number=block.page_number,
                        chunk_index=chunk_index,
                        section_heading=block.heading,
                        content=chunk_text,
                        source_type=block.block_type
                    ))
                    chunk_index += 1
                    if end == len(words):
                        break
                    start += (self.chunk_size - self.chunk_overlap)

        return chunks

chunker = StructureAwareChunker()
