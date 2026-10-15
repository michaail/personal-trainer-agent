from pathlib import Path

from garmin_fit_sdk import Decoder, Stream

ACTIVITY_PATH = Path(__file__).resolve().parents[2] / "data" / "2026-02-26-18-00-48.fit"


def read_activity(path: Path) -> dict:
    decoder = Decoder(Stream.from_file(str(path)))
    messages, errors = decoder.read()

    if errors:
        raise ValueError(f"Failed to decode {path.name}: {errors}")

    return messages


messages = read_activity(ACTIVITY_PATH)

print("Message types:", list(messages))

# Activity-level summaries
for session in messages.get("session_mesgs", []):
    print("Sport:", session.get("sport"))
    print("Timer duration, seconds:", session.get("total_timer_time"))
    print("Distance, metres:", session.get("total_distance"))
    print("Average power, watts:", session.get("avg_power"))
    print("Average heart rate, bpm:", session.get("avg_heart_rate"))

# Timestamped samples
records = messages.get("record_mesgs", [])
print("Samples:", len(records))

for record in records[:5]:
    print({
        field: record.get(field)
        for field in ("timestamp", "power", "heart_rate", "cadence")
    })