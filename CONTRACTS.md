# BU probe contracts — revision 1

Each invocation reads one UTF-8 JSON object from standard input and writes exactly one JSON object to standard output. No extra keys, diagnostics or nonfinite numbers. Only `solution.py` (regular file, at most 64 KiB) is copied into the sandbox. Python 3.13 standard library only. The source must be deterministic, require no network, dependencies, files or hardware, and complete within the execution limits. The trusted examiner tests 14 cases twice with fresh random values; this detects tested errors and inconsistent behavior, not every possible defect or every hardcoded strategy.

These are software exercises using synthetic input. A pass is **technical verification**, not an academic grade, proof of production network safety, or a measurement of hardware, SCION deployment or real routing policy.

## rpki-origin

Input: `{"routes":[{"prefix":"192.0.2.0/24","asn":64512}],"roas":[{"prefix":"192.0.0.0/16","asn":64512,"max_length":24}]}`.

Output: `{"states":["valid"]}` in input route order. Both IPv4 and IPv6 canonical network prefixes are possible. A route is `valid` when at least one covering ROA has the same ASN and permits its prefix length. It is `invalid` when at least one ROA covers it but none authorizes it. It is `not_found` when no ROA covers it. Different address families cannot cover each other. Empty routes return an empty list. Overlapping ROAs use any valid authorization.

## packet-counts

Input: `{"samples":[{"sent":10,"received":8},{"sent":5,"received":5}]}`. Samples are independent interval counts, not cumulative counters. Output: `{"sent":15,"received":13,"lost":2,"loss_fraction":0.13333333333333333}`. Counters must be nonnegative integers (not booleans), with received <= sent. Any invalid counter yields exactly `{"error":"invalid_input"}`. Empty samples give 0/0/0 and null loss_fraction. Zero sent means null fraction. Floating fractions compare within absolute 1e-9.

## readonly-policy

Input: `{"tool":"get_routes","arguments":{}}`. Output: `{"decision":"allow"}`. Exact read allowlist: `get_routes`, `get_interfaces`, `get_logs`. Exact mutation list: `set_route`, `restart_interface`, `apply_config` always yields `needs_approval`. Unknown or altered tool names yield `deny`; no trimming, case folding or prefix matching. Argument strings claiming approval have no authority. Never execute commands or access a router.

## latency-summary

Input: `{"samples_ms":[10,null,30,20]}`. Null means loss; other samples are nonnegative integer milliseconds. Output: `{"total":4,"received":3,"loss_fraction":0.25,"median_ms":20,"p99_ms":30}`. Median averages the two middle received values for even length. P99 uses nearest-rank sorted[ceil(0.99*n)-1], over received samples only. Empty input gives null fraction and latency statistics. All-lost nonempty input gives fraction 1 and null latency statistics. Booleans cannot stand in for numeric outputs; integral and decimal representations of the same value are accepted.

## path-policy

Input: `{"paths":[{"id":"a","asns":[1,2,3],"up":true},{"id":"b","asns":[1,4,3],"up":true}],"forbidden_asns":[2]}`. Output: `{"path_id":"b"}`. An eligible path is up and has no forbidden ASN anywhere. Choose the shortest AS sequence, then lexicographically smallest ASCII path ID. If none is eligible, return null path_id. IDs are unique, lower-case ASCII strings; AS paths are nonempty positive integer lists. Treat this as a path-selection exercise, not SCION connectivity evidence.
