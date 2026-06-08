export interface DocumentItem {
  id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  content_hash: string;
  page_count: number;
  processing_status: string;
  processing_error?: string | null;
  processing_duration_sec: number;
  metadata_json: Record<string, any>;
  created_at?: string;
  chunks?: ChunkItem[];
}

export interface ChunkItem {
  id: string;
  document_id: string;
  document_name: string;
  page_number: number;
  chunk_index: number;
  section_heading?: string;
  content: string;
  source_type: string;
}

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  document_name: string;
  page_number: number;
  section_heading?: string;
  content: string;
  score: number;
  retrieval_method: string;
}

export interface Citation {
  citation_id: number;
  document_id: string;
  document_name: string;
  page_number: number;
  source_passage: string;
  relevance_score: number;
  evidence_status: string;
}

export interface ChatResponse {
  answer: string;
  abstained: boolean;
  abstention_reason?: string;
  citations: Citation[];
  grounding_confidence: number;
  latency_ms: number;
}

export interface ExtractedField {
  field_name: string;
  extracted_value: any;
  source_document: string;
  page_number: number;
  supporting_passage: string;
  validation_status: string;
  evidence_status: string;
}

export interface ExtractionResult {
  document_id: string;
  schema_name: string;
  fields: Record<string, ExtractedField>;
  completeness_score: number;
  validation_errors: string[];
}

export interface DiffItem {
  category: string;
  attribute_name: string;
  value_a: string;
  value_b: string;
  difference_summary: string;
  evidence_a: string;
  page_a: number;
  evidence_b: string;
  page_b: number;
  is_conflict: boolean;
  verification_status: string;
}

export interface ComparisonResult {
  comparison_id: string;
  document_a_name: string;
  document_b_name: string;
  category: string;
  differences: DiffItem[];
  conflict_count: number;
}

export interface AgentStepTrace {
  step_number: number;
  action: string;
  tool_name?: string;
  tool_input?: any;
  tool_output?: any;
  timestamp: string;
}

export interface AgentRunResult {
  run_id: string;
  goal: string;
  status: string;
  steps: AgentStepTrace[];
  final_output?: string;
  duration_sec: number;
}
