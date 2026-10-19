---
depth: tactical
id: EVID-006
kind: evidence
last_modified_at: 2026-10-18T19:50:12.268383+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: SPEC-001
  relation: informs
status: active
title: Independent catalogue contract review — frozen SPEC-001 — reviewer catalog spec 20261018 01
---

# EVID-006: Independent catalogue contract review of frozen SPEC-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-18 |
| Valid Until | Not set; revision-specific review |
| Target | SPEC-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: reviewer/catalog-spec-20261018-01
reviewer_role: artifact-reviewer
generator_identity: creator/catalog-spec-20261018-01
reviewed_artifact_id: SPEC-001
reviewed_artifact_updated_at: 2026-10-18T19:44:40.337539+00:00
review_verdict: PASS

## Measurement

Independent forgeplan_reviewer document inspection, exclusively artifact-reviewer; maintainer and generator identities remain distinct. Read AGENTS.md, reviewer TOML, complete original /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt, complete scoped get NOTE-001/SPEC-001 and .forgeplan/specs/SPEC-001-coworking-nearby.md. Reread large outputs in bounded portions. NOTE-001 metadata: active, standard, updated_at=2026-10-18T18:29:58.718062+00:00.

Scoped health: healthy, total=8 before this Evidence, four advisory phase mismatches. Scoped new/get inspected actual Evidence template; exactly one new Evidence with parent_id=SPEC-001 and automatic informs. No delegation, reason/score/activation, target/source/test edits or guard changes.

Read-only cat/sed inspected documents. Python hashlib.sha256 of exact get body returned 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8; get timestamp matched assigned pin. Projection standard/draft with based_on NOTE-001; extracted body matches get after removing trailing newlines, raw equality false from newline separation. Frontmatter last_modified_at is not database updated_at. No implementation or application tests were run.

## Result

PASS for source fidelity and substantive internal consistency of this proposed catalogue contract. Reviewed all 13 field rows, C01–C08, all 24 T01–T24 scenarios and FR/AC boundary traces. No blocking catalogue-contract inconsistency found. This is a document review, not approval of the proposals, production data, implementation or a Standard activation gate.

## Findings

1. Closed model and normalization challenged against original §4.
The table contains exactly id, name, address, latitude, longitude, active, yandex_maps_url, short_review, description, rating_text, rating_source, rating_checked_at and updated_at: 5 required plus 8 optional, no added application field. Required strings have no defaults, reject omitted/null/nonstring/blank; active defaults only on omission and rejects null, empty string and numeric booleans. Nullable optional strings map omission/null/trim-blank to missing keys. rating_source omission/blank defaults catalog, null fails, exact catalog/yandex only. 

Required-string trim is a NEW explicit proposal, not a source mandate. C04 names its exact Unicode trim set, applies length after trim and preserves inner content. IDs are case-sensitive after trim: " a " collides with "a"; "a" differs from "A". No NFC/NFKC: visually equivalent IDs may differ, an owner usability risk. Length uses code points, not bytes/graphemes; one astral scalar counts one, combining sequences may count more. Unpaired surrogates fail. Required limits 64/150/250 and optional limits 200/500/50 match §4. Unpaired surrogate rejection makes scalar-content preservation coherent. Approval must consciously accept these new normalization choices.

2. Whole-file parsing and diagnostics challenged with late and inactive failures.
C01–C03 require strict UTF-8 JSON array-of-objects, complete ordered success including inactive or failure without partial list; shared startup/offline validator, before polling. Duplicate JSON members fail separately from duplicate IDs and unknown fields. BOM/surrogate rules are proposals. Diagnostics give path/class/field/id-or-index; file-level failures use N/A and $file/$json/etc. Empty bytes or whitespace-only input cannot form a JSON array, so fail as JSON; [] succeeds with zero records. Missing file is configuration failure, never [] or demo fallback. This distinction is entailed by C01 although T21 does not separately name the zero-byte fixture.

Fail-fast need not collect all defects. C02/T20/T22 forbid filtering invalid inactive or late records. Offline needs no token/network; command names, exit codes and parser representation belong to RFC.

3. Numeric and date edge conditions challenged.
C04 permits finite JSON integer/fraction/exponent values, excludes bool/string/null/nonfinite, and checks inclusive latitude [-90,90], longitude [-180,180]. Zero, negatives, boundaries and same coordinates with distinct IDs remain valid. T07 rejects overflow becoming nonfinite. Numeric value is preserved, not lexical spelling; no ll inference.

C07 requires Gregorian ASCII YYYY-MM-DD, years 0001–9999, leap centuries and real days. Present dates always validate, with no invented freshness/future/order restrictions. C08 requires valid URL/date only when normalized rating_text is present and source=yandex; null/blank cannot satisfy dependencies. Without rating, yandex needs neither, but invalid present optional values still fail. Catalog text is not rescaled or turned into zero; §3/4 and AC-10/11 preserved, display integration deferred.

4. Concrete URL allowlist challenged as an unapproved project proposal.
C06 permits exactly yandex.ru and yandex.com, absolute HTTPS, ASCII-insensitive scheme/host, raw path exactly /maps or prefix /maps/. No port or literal :443 only; :0443, empty/other/nonnumeric ports fail. Userinfo including empty, www/wildcard subdomains, suffix traps, trailing dot, encoded host, IP/IDN lookalikes fail. Thus https://yandex.ru/maps and HTTPS://YANDEX.RU:443/maps/ are syntactically eligible, whereas https://yandex.ru.evil/maps, https://www.yandex.ru/maps, https://@yandex.ru/maps, https://yandex.ru:0443/maps and https://yandex.ru/mapsx fail under the written policy.

C06 rejects raw controls/whitespace/backslash, malformed encoding and path slash/dot evasions without browser repair or premature decoding. Query/fragment are data, not coordinates. This is document analysis, not parser execution. The proposal rejects ya.ru/non-maps links; it is neither approved nor an exhaustive official host list. No fetch, scraping, API or shortlink resolution. Residual risks: legitimate rejected links, future host drift, parser mistakes and unverified branch correspondence.

5. Owner semantics and source restrictions challenged.
C05 retains city-plus-house and same-branch correspondence as owner duties, while syntax checks only nonblank bounded address. Original "Москва, тестовый адрес" lacks a house number: it is labelled illustration, not approved real data or a geocoding promise. T24 separates these obligations; ll/address cannot replace named coordinates. Texts/ratings come from owner, without generated attributes or enrichment. Loading is read-only, updates require restart, synthetic fixtures stay labelled and never automatically replace real data. [] is valid but useful service needs real owner data.

6. All 24 scenario oracles and traceability challenged.
T01–T05 cover defaults, required variants, exact/over code-point limits, nullable blanks and strict types; T05's broad wrong-type wording includes booleans but its explicit "only active true/false accepted" clause correctly carves out active. T06–T09 cover numeric limits/invalids, same coordinates, normalized duplicate/case-sensitive IDs and unknown fields. T10/T11 cover calendar successes/failures and no freshness. T12–T16 cover positive host/port/path syntax and negative authority/path/encoding/shortlink cases. T17/T18 cover conditional ratings and independently invalid optional values. T19 covers empty/one/two/inactive catalogues while deferring selection. T20/T22 cover atomic inactive/late failure and shared offline/startup behavior. T21 covers file/encoding/JSON/root/entry/duplicate-member diagnostics. T23 preserves source text beyond proposed trim without asserting renderer checks passed. T24 covers semantic address ownership and explicit-coordinate requirement.

The 24 rows are future test families, not executed tests or exhaustive parser proof. Explicit zero-byte JSON, lone-surrogate and more Unicode/double-encoding fixtures remain expansion cases; written rules control. FR-03/06 traces stop at list obligations; FR-08/AC-10/11 own text/source/dependencies, AC-12/14 loading/errors. Active filtering AC-05, sort AC-06, origin/distance AC-13 and renderer AC-15 remain integration work. FR-07/AC-07/08 route generation and rounding/formatting were excluded. No whole-product acceptance or card-size verification claimed.

7. Minor provenance wording, not an application blocker.
SPEC risk 6 calls the refused reason attempt isError=true. User-provided event context says wrapper status=failed/result=null/error.message; refusal text is accurate. Earlier event was not rerun or freshly observed. This wording discrepancy does not imply successful reasoning, provider diagnosis or application failure. ADI/Guardian/gate remain pending.

## Interpretation

PASS supports this frozen proposed document only. Trim/URL/strict-input choices still need approval; implementation verification, semantic owner checks and independent ADI/Guardian/gates remain separate. No activation, including future Evidence activation, is authorized. Guards unchanged.

## Congruence Level Justification

CL3: exact target revision/projection, active parent and full original in this workspace. Measurement means document counts/pin/consistency inspection, not runtime tests.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| SPEC-001 | informs (automatic parent link from this Evidence) |

Freeze protocol: scoped validate/get Evidence and get SPEC-001 after saving; report final Evidence revision and target pin comparison. Leave draft, standard depth; no further body edits after freeze.



