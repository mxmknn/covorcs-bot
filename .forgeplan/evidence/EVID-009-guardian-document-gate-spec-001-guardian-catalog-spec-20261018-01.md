---
depth: tactical
id: EVID-009
kind: evidence
last_modified_at: 2026-10-18T20:05:48.953766+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: SPEC-001
  relation: informs
status: active
title: Guardian document gate — SPEC-001 — guardian/catalog-spec-20261018-01
---

# EVID-009: Независимый Guardian review SPEC-001

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-18 |
| Valid Until | Revision-specific; metadata valid_until не задано |
| Target | SPEC-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3

## Review Metadata

reviewer_identity: guardian/catalog-spec-20261018-01
reviewer_role: guardian
generator_identity: creator/catalog-spec-20261018-01
reviewed_artifact_id: SPEC-001
reviewed_artifact_updated_at: 2026-10-18T19:44:40.337539+00:00
guardian_verdict: PASS

## Measurement

Независимо прочитаны AGENTS.md, Guardian TOML, весь SPEC-001, active EVID-006/EVID-007, active NOTE-001 и отдельно весь оригинал /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt. Сверены 13 полей, C01–C08, T01–T24, provenance и gates.

Exact get: Standard/draft, body 24272 символа, SHA256 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8, pin совпал. Повторный CLI get после создания собственного EVID дал тот же timestamp/hash; проекция после rstrip совпадает. Hash вычислен Python в памяти. Первый print получил KeyError r_eff_score из-за имени CLI cache r_eff; исправленный read-only вызов успешен.

## Result

PASS только для предложенного документа SPEC-001 указанной ревизии. Неразрешённых BLOCKER в пределах локального контракта не выявлено. Applicable S10–S13: 8/8, 100%; каждый слой 2/2, C4 N/A для kind spec. Для Standard нужен один независимый artifact-reviewer: он есть; generator, reviewer, evidence-gatherer и Guardian имеют разные identities. Этот PASS не одобряет новые политики за владельца и не заменяет активацию или будущую проверку реализации.

Свежая оценка выполнена ДО создания EVID-009 командой forgeplan context SPEC-001 --json на ForgePlan 0.33.0: artifact.r_eff=0.9, derived_status=EVIDENCED, FGR reliability=0.851, formality=0.75, granularity=0.4, grade B; validation passed, must_errors=0, should_warnings=0. Cached scoped get r_eff_score=0.0 и CLI r_eff=0.0 — сохранённый cache, не свежая оценка. forgeplan_score/score-all не вызывались, target score/timestamp не сохранялись.

## Findings

1. Слабейшая опора — документальная индукция. EVID-007 содержит manual ADI A–D: shared целый снимок выбран, permissive parser, do-nothing/scope-reduction и enrichment отвергнуты с tradeoffs/фальсификаторами. Автоматический reason не выполнен из-за approval refusal. Это поддерживает согласованность контракта, но не качество реальных записей, false-negative долю URL, спрос или работающий валидатор. Следующее доказательство — независимые runtime проверки после законного RFC/unlock-build.

2. Свежесть/независимость проверены по фактическим metadata, а не таблицам Status в body. EVID-006 active/tactical, updated_at=2026-10-18T20:00:42.063072+00:00, reviewer_role artifact-reviewer, reviewer/catalog-spec-20261018-01, review_verdict PASS, точные target ID/revision. EVID-007 active/tactical, updated_at=2026-10-18T20:00:42.467851+00:00, evidence-gatherer evidence/catalog-spec-adi-20261018-01, точный pin/hash. Оба informs SPEC-001 в YAML и graph, оба созданы после target revision; valid_until=null не делает их применимыми к будущему изменению SPEC. Их body Status Draft — историческая запись до активации, фактический status active. Guardian не генератор и не один из этих verifiers. Требование двух artifact-reviewer identities относится к Critical, target Standard.

3. C01–C03 сохраняют UTF-8 JSON array, ordered complete normalized list либо отказ, общий будущий offline/startup validator и отсутствие polling до полного успеха. Ошибка последней или inactive записи отклоняет весь файл. Fail-fast не требует собрать все ошибки. Диагностика: path/class/field/id либо zero-based index, для file/encoding/JSON/root N/A. [] success отличается от missing/unreadable failure; demo fallback запрещён. Offline без token/сети; имя команды/exit codes/wiring определит RFC.

4. C04 включает ровно id/name/address/latitude/longitude/active/yandex_maps_url/short_review/description/rating_text/rating_source/rating_checked_at/updated_at. Пять required без defaults. Required strings отвергают missing/null/blank/nonstring, лимиты 64/150/250; id уникален case-sensitive после предлагаемого trim. Nullable optional string missing/null/blank дают отсутствие ключа; лимиты short_review/description/rating_text 200/500/50. active default true только при omission, false сохраняется, null/blank/0/1/string не boolean. rating_source omitted/blank становится catalog, null неверен, exact catalog/yandex без folding. Coordinates finite JSON number с inclusive ±90/±180, zero/negative/fraction/exponent разрешены, bool/numeric string/null/nonfinite запрещены; одинаковые coords разных id допустимы. Numeric value не lexical spelling. Типы не приводятся, unknown keys отвергаются.

5. Trim exact Unicode set, code-point lengths, required trim, normalized id uniqueness, отсутствие NFC/NFKC, BOM/unpaired-surrogate и duplicate-member rejection явно помечены PROPOSAL. Это новые проектные решения, а не дословный intake. Сохранение текста означает всё кроме предложенного outer trim; внутренние пробелы, регистр и содержимое не переписываются. Визуально одинаковые Unicode IDs могут различаться; BOM-файл редактора может отклоняться. Эти цены должны быть осознанно приняты при отдельном SPEC approval. Reviewer не получил полномочий сделать такое approval.

6. C06 также proposal: только exact yandex.ru/yandex.com, HTTPS с ASCII-insensitive scheme/host, raw path /maps либо /maps/, порт отсутствует или literal 443. Userinfo даже пустой, www/subdomains/suffix traps/trailing dot/encoded host/IDN/IP, :0443/пустой/иной port запрещены. Case-sensitive path, dot-segment/encoded slash/backslash и percent/control ограничения описаны без browser repair. Query/fragment данные, не источник координат. Narrow policy может отвергать реальные полезные ссылки; она не официальный полный allowlist. Исходник требует HTTPS/explicit allowlist, но не эти exact hosts/path/port. Синтаксически допустимый synthetic URL не доказывает существование страницы или филиал. Проверка URL локальная; route URLs FR-07/AC-07–08 не смешаны с карточкой организации. Для одобрения надо принять эти ограничения либо вернуть proposal на отдельное решение; Guardian их не изменяет.

7. C05 правильно оставляет городу/дому и соответствию name/address/coords/link одному филиалу владельческую semantic acceptance. Непустой address без дома может пройти schema и всё ещё не пройти owner acceptance; это не отмена исходного требования полного адреса. Иллюстративная Москва/тестовый адрес не стала настоящим местом. URL/ll/адрес не заменяют named coordinates. Real [] допустим до входов владельца, labelled synthetic хранится отдельно без автоматической подстановки.

8. C07/C08 внутренне согласованы: Gregorian ASCII YYYY-MM-DD, годы 0001–9999, leap-century cases, никакого придуманного today/freshness/order ограничения. Только present normalized rating_text вместе с yandex требует valid present URL/date. Обsolete безусловный predicate по одному yandex не применяется. Даже вне условия любое present поле валидируется. Null/blank не удовлетворяют dependency. catalog не переименован в Яндекс, отсутствующий рейтинг не превращён в zero, текст не переводится на шкалу; ДД.ММ.ГГГГ и source labels относятся к будущему renderer.

9. Все 24 GWT рассмотрены: T01–05 defaults/required/length/missing/types; T06–09 числа/same coords/id/unknown; T10–11 даты; T12–16 URL positive/authority/port/path/encoding/shortlinks; T17–18 conditional ratings; T19 размеры/inactive; T20 invalid inactive; T21 file/encoding/JSON/root/entry/member; T22 atomic shared failure; T23 text; T24 owner boundary. Это будущие семейства тестов. T05 явно разрешает active boolean. Zero-byte JSON, lone surrogate и расширенные Unicode fixtures нужны реализации; нормативные C01/C04 уже их ограничивают. AC-05/06/13/15 требуют интеграции. URL length/escaping/card assembly остаются RFC, вместимость карточки сейчас не доказана.

10. Provenance refusal — minor точность, не BLOCKER. Creator пишет isError=true; заданный контекст CLI события имеет status failed, result null и точный error.message «MCP tool call requires approval, but approval policy is never». Это разные оболочки отказа; отказ и отсутствие reasoning output описаны верно. EVID-007 отдельно сообщает собственный MCP isError=true и manual ADI, не выдаёт его за tool output. Исторический creator вызов Guardian не повторял, provider не диагностировал. Следующая передача должна сохранять различие оболочек; runtime/test PASS из отказа не следует.

11. Команды: forgeplan health — healthy, 10 artifacts, 8 advisory phase mismatches. После python3 .codex/forgeplan-methodology-gate.py --help выполнена поддерживаемая python3 .codex/forgeplan-methodology-gate.py SPEC-001 --mode methodology --json: passed=true, 8/8. Прочитана логика S10 hypotheses/S11 reviewer/S12 parent/S13 validation; boolean дополнен содержательной проверкой. guardian_detail «N/A for Tactical depth» — общий текст methodology mode, не глубина target и не свежий Guardian PASS. C4 N/A для spec. Scoped validate и forgeplan validate SPEC-001 --json: 0 errors/0 warnings. SHOULD body-links-drift не воспроизведён: actual YAML содержит based_on NOTE-001 и informs обоих EVID, graph согласован. Возможный дефект frontmatter_map не принят за установленный факт.

12. Active NOTE-001 standard updated_at=2026-10-18T18:29:58.718062+00:00 совпадает с parent_revision; PARENT_RULES разрешает spec based_on active note. Graph без цикла вокруг target. Позже появился EVID-008 informs PRD-001, он не evidence target и не использован. Phase SPEC validate, history shape/validate advisory; pipeline status route 1/standard/phase prd/dev_unlocked=false. Это не разрешение Build. Исторические pending строки creator не являются текущим gate report и не исправлялись.

## Interpretation

Следующий шаг main maintainer: проверить frozen draft Evidence, отдельно обработать его Standard gates/metadata; законная активация Evidence предшествует target и требует отдельно разрешённого SPEC approval. Новая активация сейчас не разрешена. Изменение target делает review устаревшим. RFC определит реализацию и integration oracles; Build заблокирован до readiness/unlock-build. Source/test/target/чужие artifacts, hooks/config/scripts не изменены; bypass/reason/score mutations не выполнялись. Создан ровно один EVID с parent_id, обновляется только он, default Standard сохранён.

## Congruence Level Justification

CL3: прямой exact-revision review локального target, его active parent, двух независимых active свидетельств и оригинального задания в одном workspace. CL не означает выполненные runtime/live проверки. Внешние ссылки §15 — provenance источника, не новая аттестация документации. Спрос, live интеграции и реальные данные не сертифицируются.

## Related Artifacts

| Artifact | Relation |
|----------|----------|
| SPEC-001 | informs, автоматически parent_id при создании |

После update — scoped validate/get, итоговый exact body hash и повторный get/hash target; это freeze, дальнейших правок EVID не будет.



