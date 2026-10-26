#!/usr/bin/env python3
"""EMM Armageddon random event coverage gates: do not treat AC deltas as full effects."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
events=json.loads((root/"docs/data/emm-armageddon-event-triggers.json").read_text())
choices=json.loads((root/"docs/data/emm-armageddon-event-choices.json").read_text())
assert events["commit"]==choices["commit"]=="60b0ec3740083162aaab7bf8491761a54a65a610"
assert len(events["events"])==23
all_choices={y["id"]:y for x in events["events"] for y in x["choices"]}
assert len({x["id"] for x in events["events"]})==23
assert len(choices["eventChoices"])==52
for source in choices["eventChoices"]:
    ch=all_choices[source["id"]]
    assert ch["acDelta"]==source["delta"],source["id"]
    assert "iGlobalCounter" in ch["fields"]
for trigger in events["events"]:
    c=trigger["criteria"]
    assert c["weight"]>0,trigger["id"]
    assert 0<c["percentGamesActive"]<=100
    assert len(trigger["acChoices"])>=1
# This is deliberate: an AC-only callback must never count as full event implementation.
for name in ("EVENT_HOLY_CHILD_2","EVENT_WITCH_1","EVENT_DEMONIC_TOME_1"):
    assert set(all_choices[name]["fields"])-{"Type","Description","Button","Civilopedia","iGlobalCounter"}
print("PASS: 23 pinned triggers and all 52 AC choices, including original prerequisites and non-AC effects")
print("REMAINING: runtime trigger scheduling, full eligibility, player choice UI, all other effects and Python callbacks")
