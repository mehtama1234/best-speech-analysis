import type { PracticeRecord } from "../generated/shared_evidence_contract";

export type LessonEvidence = {
  lesson_id: string;
  pattern_id: string;
  canonical_job: string;
  exact_examples: Array<{ segments: Array<{ evidence_id: string }> }>;
  delivery_samples: Array<{ sample_id: string }>;
  status: string;
  claim_level: string;
  safety_boundary: string;
};

export function createPracticeRecord(
  lesson: LessonEvidence,
  participantCode: string,
  accessibilityOrModality: string,
  stepResponses: Record<string, string>,
  savedAt = new Date().toISOString(),
): PracticeRecord {
  if (!participantCode.trim()) throw new Error("participant code is required");
  if (lesson.status !== "provisional_not_validated") throw new Error("lesson is not a provisional lesson");
  if (lesson.claim_level !== "practice_hypothesis") throw new Error("lesson is not a practice hypothesis");
  if (!lesson.safety_boundary.trim()) throw new Error("lesson safety boundary is required");
  return {
    record_type: "local_communication_practice_record",
    schema_version: "1.0",
    lesson_id: lesson.lesson_id,
    pattern_id: lesson.pattern_id,
    canonical_job: lesson.canonical_job,
    source_evidence_ids: lesson.exact_examples.flatMap(example => example.segments.map(segment => segment.evidence_id)),
    delivery_sample_ids: lesson.delivery_samples.map(sample => sample.sample_id),
    participant_code: participantCode,
    consent: true,
    accessibility_or_modality: accessibilityOrModality,
    step_responses: stepResponses,
    claim_boundary: "Local practice log only; not learner-validation evidence or effectiveness evidence.",
    saved_at: savedAt,
  };
}

export function changedResponses(previous: PracticeRecord, latest: PracticeRecord): string[] {
  const before = (previous.step_responses as Record<string, string>) || {};
  const after = (latest.step_responses as Record<string, string>) || {};
  return [...new Set([...Object.keys(before), ...Object.keys(after)])]
    .filter(key => before[key] !== after[key])
    .sort();
}
