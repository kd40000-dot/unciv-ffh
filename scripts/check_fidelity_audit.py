#!/usr/bin/env python3
"""Validate the permanent 25-system fidelity ledger, and flag unaudited gameplay commits."""
import json, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCORE=ROOT/'docs/data/fidelity-scorecard.json'
PAGE=ROOT/'docs/permanent-fidelity-audit.md'
def validate():
    data=json.loads(SCORE.read_text())
    systems=data['systems']
    assert data['schemaVersion']==1
    assert len(systems)==25, 'Exactly 25 systems required'
    assert [x['id'] for x in systems]==[f'F{i:02}' for i in range(1,26)]
    for s in systems:
        for key in ('title','status','sourcePaths','portEvidence','gameplayConfirmed',
                    'verification','remainingDifferences','lastReviewed','updatedBy'):
            assert key in s, (s['id'],key)
        assert isinstance(s['percent'],int) and 0<=s['percent']<=100, s['id']
        assert s['status'] in ('missing','early','partial','needs QA','faithful'),s['id']
        assert isinstance(s['sourcePaths'],list) and len(s['sourcePaths'])>0,s['id']
        assert isinstance(s['portEvidence'],list) and len(s['portEvidence'])>0,s['id']
        assert isinstance(s['gameplayConfirmed'],list),s['id']
        assert s['remainingDifferences'].strip(),s['id']
        assert s['verification'].strip(),s['id']
    assert PAGE.exists()
    text=PAGE.read_text()
    for s in systems:
        assert f"| {s['id']} |" in text, s['id']
    return systems

def changed_files():
    try:
        base=subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()
        return set(subprocess.check_output(['git','diff','--name-only',base,'HEAD'],text=True).splitlines())
    except (subprocess.CalledProcessError,FileNotFoundError):
        return set()

def check_change():
    files=changed_files()
    gameplay={f for f in files if f.startswith('jsons/') and f.endswith('.json')}
    gameplay|={f for f in files if f.startswith(('core/','engine/','android/core/'))}
    if gameplay and str(SCORE.relative_to(ROOT)) not in files:
        raise AssertionError('Gameplay files changed without updating docs/data/fidelity-scorecard.json: '+', '.join(sorted(gameplay)))

def main():
    systems=validate()
    avg=sum(x['percent'] for x in systems)/25
    if '--check-change' in sys.argv:check_change()
    print(f'Fidelity scoreboard: {len(systems)} systems; mean {avg:.1f}%; baseline 11.8%')
    if '--summary' in sys.argv:
        for s in systems:print(f"| {s['id']} | {s['title']} | {s['percent']}% |")
if __name__=='__main__':main()
