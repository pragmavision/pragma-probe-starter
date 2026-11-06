"""Implement one contract from CONTRACTS.md. Only Python's standard library is available."""
import json
import math
import sys

data = json.load(sys.stdin)
# Start with latency-summary, then implement another challenge in a new commit.
values = sorted(v for v in data['samples_ms'] if v is not None)
n, total = len(values), len(data['samples_ms'])
result = {
    'total':total,'received':n,'loss_fraction':(total-n)/total if total else None,
    'median_ms': (values[n//2] if n % 2 else (values[n//2-1]+values[n//2])/2) if n else None,
    'p99_ms': values[math.ceil(.99*n)-1] if n else None,
}
print(json.dumps(result))
