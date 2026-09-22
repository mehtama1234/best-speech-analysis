import type { MobileLesson } from "../generated/shared_evidence_contract";

export type MobileLessonStep = {
  step_id: string;
  type: string;
  prompt: string;
  [key: string]: unknown;
};

export type MobileLessonPayload = Omit<MobileLesson, "steps" | "evidence_links"> & {
  steps: MobileLessonStep[];
  evidence_links: {
    exact_example_ids?: string[];
    delivery_sample_ids?: string[];
    counterexample_types?: string[];
    [key: string]: unknown;
  };
};

/** Select one bounded practice stage without turning a lesson into a score. */
export function selectLessonStep(lesson: MobileLessonPayload, stepId: string): MobileLessonStep {
  if (lesson.status !== "provisional_not_validated") throw new Error("lesson is not a provisional lesson");
  if (lesson.claim_level !== "practice_hypothesis") throw new Error("lesson is not a practice hypothesis");
  if (!String(lesson.safety_boundary || "").trim()) throw new Error("lesson safety boundary is required");
  const step = lesson.steps.find(candidate => candidate.step_id === stepId);
  if (!step) throw new Error(`lesson step not found: ${stepId}`);
  return step;
}

export function linkedEvidenceIds(lesson: MobileLessonPayload): string[] {
  return [...new Set(lesson.evidence_links.exact_example_ids || [])].sort();
}
