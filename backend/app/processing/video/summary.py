from collections import Counter

def build_video_summary(detections: list[dict]) -> str:
    all_objects = []

    # Collect all objects across frames
    for d in detections:
        objs = d.get("detections", [])
        all_objects.extend([obj["object"] for obj in objs])

    if not all_objects:
        return "Video contains no detected objects."

    counts = Counter(all_objects)
    unique_objs = ", ".join(counts.keys())
    count_text  = ", ".join(f"{obj}={cnt}" for obj, cnt in counts.items())

    # Build per-frame breakdown (optionally using timestamps)
    per_frame = []
    for d in detections:
        objs = d.get("detections", [])
        if not objs:
            continue
        ts = d.get("timestamp")
        obj_list = ", ".join([obj["object"] for obj in objs])

        if ts:   # timestamp exists
            per_frame.append(f"At {ts:.1f}s: {obj_list}")
        else:    # fallback to frame index
            per_frame.append(f"Frame {d['frame_index']}: {obj_list}")

    per_frame_text = " ".join(per_frame)

    return (
        f"Video contains objects: {unique_objs}. "
        f"Counts: {count_text}. "
        f"Details: {per_frame_text}"
    )
