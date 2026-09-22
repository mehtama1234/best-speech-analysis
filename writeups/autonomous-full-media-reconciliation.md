# Autonomous full-media reconciliation

Status: **all-video proxy coverage reconciled; delivery interpretation is not claimed**.

This reconciles local media availability and generated feature proxies for every fixed-corpus video. It does not claim that media is the correct source, that a speaker/event is identified, or that any measured feature has social meaning or effectiveness.

The report covers **395 videos**. It records local media state, feature-report availability, audio/frame proxy fields, transcript alignment and missingness.

## Coverage counts

| Dimension | Counts |
|---|---|
| `media_state` | `derived_features_only`=5; `raw_audio_video_present`=354; `transcript_only_no_local_media`=35; `video_only`=1 |
| `proxy_status` | `feature_proxy_available`=357; `no_feature_proxy_report`=38 |
| `audio_measurement_status` | `not_available`=38; `rms_zcr_spectral_centroid_and_coarse_spectral_pitch_proxy; not_a_validated_pitch_tracker`=357 |
| `visual_measurement_status` | `not_available`=38; `scene_pixel_features_only; face_expression_not_analyzed`=5; `scene_pixels_plus_optional_haar_geometry; no_emotion_or_intent_inference`=352 |
| `aligned_transcript_status` | `aligned_proxy_available`=357; `not_available_or_zero`=38 |

## How to use it

Use a row to locate a source clip or to decide that a delivery claim cannot be inspected locally. Combine it with the transcript lesson and the bounded practice questions; never turn a proxy value into a claim about emotion, confidence, intent, gesture meaning or persuasion.

The [autonomous delivery reconciliation](autonomous-delivery-reconciliation.md) contains the smaller 36-sample job-linked inspection layer with bounded frame notes and practice questions.
