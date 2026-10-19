---
depth: standard
id: NOTE-002
kind: note
last_modified_at: 2026-10-18T23:43:22.579730+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-001
  relation: based_on
status: draft
title: Brief proposal — Рабочая Москва и /about — отдельный будущий Row 3 Standard
---

# NOTE-002: Brief/proposal — Рабочая Москва и /about

| Field | Value |
|-------|-------|
| Status | draft |
| Created | 2026-10-18 UTC (server metadata); task date 2026-10-19 Europe/Moscow |
| Valid Until | metadata null; tool advises NOTE expiry in 90 days, not a publication deadline |
| Context | Separate future Row 3 Feature in existing service / SPARC plus Hexagonal / Standard |

## Note

Авторизовано ровно: «Подготовить отдельное изменение для „Рабочей Москвы“ и /about». Предлагается ограниченный будущий переход отображаемого бренда к «Рабочая Москва: места для учёбы и работы» и команда /about с дословным supplied editorial text. Это подготовка отдельного цикла после текущего Coworking Nearby Row 1 Standard Build, а не расширение его разрешения. Для отдельного изменения нет active Brief, PRD или RFC; этот draft не даёт Build unlock и не меняет RFC-001, pipeline или работу sole EDGE coder.

## Related

| Artifact | Relation / meaning |
|----------|--------------------|
| NOTE-001 | based_on, только историческое происхождение и контекст; active parent, updated_at 2026-10-18T18:29:58.718062+00:00 |
| PRD-001 | active baseline context only, updated_at 2026-10-18T20:51:11.875851+00:00; новая dependency link не предлагается |
| SPEC-001 | active baseline context only, updated_at 2026-10-18T20:51:12.611918+00:00 |
| RFC-001 | active compatibility baseline only, updated_at 2026-10-18T21:37:59.988494+00:00; canonical MCP body SHA256 e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 |

based_on не означает, что NOTE-001 разрешает новый бренд, /about или редакционный импорт. Link auto_activate_source_if_complete=false. Metadata active существующих документов имеет приоритет над их исторической draft-прозой.

## Attribution, read context and limits

generator_identity: creator/moscow-change-20261019-01
generator_role: ForgePlan Role A / creator
depth: standard
workspace: /Users/mxmknn/Documents/ChatGPT/tg-bot-org
source_path: /Users/mxmknn/.codex/attachments/4f27a128-c13f-4396-bc31-0be0fcbbfa65/Pasted text.txt

Прочитаны AGENTS.md, полный creator contract, role-scoped MCP authorization rules, installed NOTE template (из установленного binary 0.33.0), workspace config, current pipeline и active NOTE/PRD/SPEC/RFC. NOTE template содержит Note и Related; его пример Status Active заменён на реальное draft. Прочитан существующий render и relevant Telegram adapter контекст; data/coworkings.json реально []. Git unborn по входному контексту: HEAD/commit не назначены, Git не изменяется. No runtime tests or live verification performed.

Health read: healthy, 26 artifacts, 22 advisory phase mismatches (не gate PASS). Pipeline read: version 1, route 1, standard, phase build, dev_unlocked true, brief NOTE-001, prd PRD-001, rfc RFC-001, updated_at 2026-10-18T22:32:21.392420+00:00. Advisory session coding, active_artifact null; он не заменяет pipeline и не маршрутизирует новый scope. Эти наблюдения — снимок concurrent Build, не обещание неизменности чужих файлов. Никаких session/metadata/pipeline/older-artifact mutations этим creator.

## Goals and proposed users

Для пользователя личного чата: понятное редакционное название проекта и доступный культурно-образовательный контекст через /about, без обещаний готового рабочего места. Для владельца: отдельный проверяемый scope и provenance текста, который можно передать в будущие PRD/RFC, не смешивая редакционные материалы с геокаталогом. Измеренный спрос, рост аудитории, SLA и экономический эффект неизвестны; успех предложения определяется будущими acceptance oracles, не выдуманными метриками.

## Bounded future scope and display surfaces

Все поверхности ниже PROPOSED, не уже разрешённые изменения:
1. Заголовок/приветствие /start: отдельная строка «Рабочая Москва: места для учёбы и работы» перед существующей инструкцией. Точный approved baseline instruction и динамический RESULTS_LIMIT сохраняются; это предпочтение для будущего PRD, не rewrite сейчас.
2. /help: отдельная строка бренда и discovery «/about — о проекте», с сохранением объяснений геопозиции, каталога владельца и расстояния по прямой.
3. /about в private chat: полное exact about.text из Appendix A; brand header и provenance при необходимости отдельны от exact text, порядок/формат таких дополнений — открытый выбор.
4. Telegram command menu: предложение добавить /about для discoverability; решение и eventual operator step только в будущем цикле. Никаких BotFather/API действий сейчас.

Account display name, username, avatar, package/module names, repository name, README/config переименование не входят в это bounded proposal; нужны отдельные решения, если потребуются. Существующие approved Coworking Nearby тексты остаются implemented baseline до activation отдельного scope; no rename now.

Proposed acceptance behavior в группе: /about проходит существующую безопасную ветку перенаправления в private chat («Открой личный чат с ботом и отправь геопозицию»), без полного editorial ответа и без group search. Менять wording group redirection не требуется. /about должен распознаваться как отдельная команда раньше generic text fallback в личном чате; @bot suffix/аргументы и чужой @username требуют явного решения будущего PRD с учётом существующего dispatch, не скрытого расширения.

## Non-goals

Не импортировать девять карточек или partial rsl_main; не создавать положительные/отрицательные amenities, рейтинги, описания или рекомендации из неизвестного. Вне scope photos/downloads/licensing, automatic geocoding, entrance discovery, new ranking, eligibility changes, runtime resources/dependencies/services, новые каталожные поля, live hours/seats guarantees. Не добавлять обязательные фичи, API calls, web research, Telegram verification или deployment. Complete input + separate validation/authorization нужны до любого расширения редакционного импорта.

## Source integrity and partialness

Source bytes independently read unchanged: 11151; SHA256 47ec52b6680bc00edd119d7457798c62aeb780d3518797a484e8f7d686ccfbef. UTF-8 valid. Whole JSON TRUNCATED at line 96 внутри photo первой rsl_main после height 909 member; full-document parsing/repair не выполнялись. top-level about key найден отдельно, JSONDecoder.raw_decode starting at its object извлёк complete about object; text имеет 201 whitespace-separated words. Attachment сохранён unmodified, копий/исправленных файлов не создавалось.

Supplied declarations: artifact_type editorial_content; schema_name rabochaya_moskva_editorial_content; schema_version 1.0; source date/checked_date 2026-10-19 Europe/Moscow; deployment_status not_verified. Все четыре readiness flags false: production_import_ready, geocatalog_ready, live_hours_or_seats_verified, implementation_and_deployment_verified. Заявлены девять карточек/candidates, но available bytes содержат только partial first rsl_main; восемь остальных и полный candidate/source registry недоступны. verified_places — supplied название раздела, не наше factual certification.

about.source_ids exact: src_25, src_26, src_16 (в запросе сокращённо src25/src26/src16). Полные registry entries отсутствуют; supplied URLs сохранены в Appendix A. about.checked_date 2026-10-19 — дата, заявленная автором, не дата independently verified current facts. No external verification performed. Не fetch и не подтверждаем supplied assertions в этом draft.

Author interpretation отдельно: «Мы рассматриваем места для чтения и самостоятельной работы как точки знакомства с образовательной и культурной средой Москвы. Для полезного путеводителя важны и культурный контекст, и проверенные условия реального визита.» (kind author_interpretation). Последний абзац about явно содержит авторский вывод. Laptop permissions, outlets/amenities, seating, hours, temporary closures, exact entrance/coordinates и factual/source freshness остаются unknown до независимой проверки; unknown не true и не false. Municipal единый читательский билет нельзя автоматически переносить на federal libraries или самостоятельные институции. Partial rsl_main coordinates null остаются null, никогда не 0; адрес/URL не заменяет координаты. Future editorial source/store contract отделён от closed thirteen-field runtime catalog; его schema/location/lifecycle ещё не выбраны, не вводятся этим NOTE.

## Explicit hypotheses, deduction and synthesis

### Hypothesis H1 — selected bounded proposal
Display brand + exact /about + help discoverability дают согласованный контекст без изменения поиска. Поддерживается complete about и явным поручением; полезность пользователям не исследована. Цена: новые dispatch/render cases и независимая factual research перед публикацией. Falsifier: exact text cannot be safely delivered under unchanged scheduler or independent primary research contradicts supplied claims. Recommendation: только draft сейчас, future bounded cycle после текущего.

### Hypothesis H2 — do nothing
Оставить Coworking Nearby и отсутствие /about навсегда: нулевой migration/regression risk, но не реализует запрошенный будущий scope. Сохранение baseline сейчас обязательно; отказ от подготовки отвергнут. Если future research не проходит, publication остаётся заблокирована, а baseline можно сохранить.

### Hypothesis H3 — scope reduction
Только /about, без новых brand surfaces/menu: уменьшает review и rendering scope, сохраняет полный редакционный текст. Недостаток: проектный бренд остаётся несогласованным с запросом. Реальная допустимая альтернатива для будущего решения владельца, сейчас не silently selected. Ещё сильнее сокращать/пересказывать about нельзя: exact supplied text — условие этой подготовки.

### Hypothesis H4 — wait for full nine-card import
Полный редакционный набор мог бы сделать бренд полезнее, но вход truncated, нет registry/coordinates/photo rights/current checks; новый scope и риски существенно шире. Не выбран: brand/about можно планировать отдельно, импорт не является prerequisite подготовки и не разрешён к реализации.

Synthesis: H1 как bounded future recommendation; H2 сохраняет безопасный текущий baseline, H3 остаётся вариантом сокращения, H4 исключена из scope. Это creator reasoning, не independent Evidence или gate decision.

## Baseline compatibility and invariants

Active PRD/SPEC/RFC остаются нормативной baseline поиска. Не менять strict closed 13 fields, defaults, atomic validation (включая inactive), local UTF-8 array, real default [], no network fallback/demo autofill. Editorial document никогда не подставляется в runtime catalogue. Haversine R=6371000, active filtering, raw-distance sorting then id ties, min(limit,count), RESULTS_LIMIT 1–5/default3, zero/negative/distant valid coordinates и три Яндекс rtt pd/mt/auto маршрута от исходной точки сохраняются. Не вводить город/радиус, ranking/eligibility или amenities inference.

All outbound /about chunks use original command source message ReplyParameters(message_id=source_id, allow_sending_without_reply=False); deleted source means STOP, never unthreaded fallback. /about целиком — один admitted envelope через тот же ordered ingress/per-chat FIFO; chunks не interleave с location/help того же чата. Другие чаты изолированы. No task-per-command bypass; no duplicate admission, cursor/counters/successor supervision changes.

Сохраняются active-inclusive GLOBAL_PENDING64/PER_CHAT_PENDING8, fetched1/backpressure, 90s service deadline, 10s attempt timeout, full 1.1s pause before every attempt, total retry_after15s and existing finite single explicit decoded429 retry. Confirmed prefix/chunks never replay; ambiguity/5xx/timeouts stop; no transitive replay. Queue wait separate; cleanup, ownership, 16s cooperative shutdown/20s grace and fail-stop boundaries не расширяются. Если будущий текст не укладывается в эти бюджеты, конфликт возвращается в design gate, не увеличивает ресурсы автоматически.

Privacy: no token/credentials, exact origins, full route URLs, raw updates/error payload logging; transient in-memory request context released as baseline. Editorial attribution не становится логированием user data. Existing offline suite belongs to RFC-001 and does not prove /about. This creator neither ran nor certified it.

## Future acceptance oracles (all pending)

| Oracle | Required observation / decision |
|--------|---------------------------------|
| A1 exact text/provenance | Decode Appendix A vs independently extracted about.text: exact Unicode, paragraphs, punctuation and all three supplied URLs; 201 whitespace words. Preserve src_25/src_26/src_16 and supplied checked_date in editorial provenance without claiming independent verification. If research requires edits, return to separately reviewed editorial revision; do not quietly alter exact input. |
| A2 Telegram size/chunks | Measure actual proposed serialized payload and decoded displayed text with pinned Telegram limit semantics offline. Supplied 201 words alone is not size proof. One message if it fits; safe ordered chunking only if needed, at Unicode/paragraph boundaries without dropped/reordered text or split escape entities, reconstructing exact about.text (no automatic numbering inserted into source). All chunks bound to same original command; final attribution format separately specified. |
| A3 escaping | Treat source as text, never raw HTML/markup. At a single HTML transport boundary escape once using existing safe escaping; no validator/store pre-escaping and no double escaping. Decoded displayed text equals input. Offline adversarial &, <, >, quotes and astral characters test once-only escaping; source cannot inject tags. An explicit plain-text transport alternative, if chosen later, must use no HTML parse mode rather than send visible entities. |
| A4 dispatch/FIFO/groups | Private /about reaches editorial handler, /start,/help, fallback/location unchanged except proposed surfaces. Define exact suffix/argument cases before Build. Group uses existing private redirection; no full about/search. Barrier tests interleave about/location/help, two chats, deletion and partial-send failures; every response/chunk source-bound, original order and no replay. |
| A5 search regression | Original RFC acceptance and SPEC T01–T24, Haversine/order/routes/limits/source labels and strict defaults unchanged; location before start and edited_message behavior preserved. Reuse independent original oracles, not only new UI tests. |
| A6 no import | Real default [] stays [], missing/invalid catalogue retains original errors; no startup/import network calls or editorial fields injected; null coordinates cannot become zero. No cards/photos/geocoding introduced. |
| A7 publication research gate | Independent primary-source research for supplied assertions, municipal versus federal rules, current access/hours/closures and relevant laptop/seating unknowns before publishing. Full source registry needed for complete attribution. Record checked date of future research separately; unresolved claims block publication or require separately authorized revised text. |
| A8 surfaces/rollback | Future approved surface inventory has exact before/after text, preserved baseline instruction and no username/package rename; restoring prior compatible build restores original commands/text with catalogue unchanged. |

These are future tests/review obligations, no executed runtime or live results. No external research to supplied URLs performed for this draft; Appendix is a faithful proposal, not endorsed factual advice.

## Decisions and tradeoffs

Separate future cycle protects current Row1 authorization and sole EDGE ownership, at cost of delayed branding. Text fidelity preserves supplied editorial authorship but blocks silent factual correction; research conflicts need a reviewed replacement. Reusing FIFO/sender avoids a second ordering/retry policy; long text cannot justify new deadlines/resources. Keeping editorial provenance separate avoids weakening strict catalog, at cost of a later source/store decision. Limited display surfaces avoid accidental technical rename; menu remains optional proposal pending exact future scope.

## Missing inputs and unresolved constraints

Full original nine-card JSON and candidate/source registry missing; no claim that unseen cards/photos/licenses exist in usable form. For this bounded scope, primary research and exact attribution display/store policy remain required before publication. Brand surfaces, menu registration ownership, /about arguments/@suffix behavior, text transport and actual length/chunk count remain proposed until future PRD/RFC resolve them. No coordinates, entrance, amenities, rights or runtime freshness inferred. No new launch date, popularity, seating or access guarantee.

## Rollout and rollback (future only)

After future gates, release a compatible version with bounded surfaces and /about; do not run overlapping pollers or introduce runtime services. Prepublication research is required even if offline delivery passes. Roll back on text corruption, wrong dispatch/source binding, FIFO/privacy regression, factual conflict or unintended catalog changes: stop candidate through existing bounded lifecycle and restore last compatible Coworking Nearby version with unchanged owner-approved catalog. No migrations/import reversal required by bounded scope; no automatic replay of interrupted chunks/requests. If no safe version, remain stopped; existing Telegram history cannot be erased by rollback. None of these actions occur now.

## Future route and gates

Routing independently selected exactly Row 3 Feature in existing service / SPARC plus Hexagonal / Standard; no reroute call or second pipeline begin. After current cycle: Route -> Brief(active) -> PRD(active) -> RFC(active) -> Build -> Prove -> Ship for this separate change. This NOTE is only a candidate Brief/proposal. Before every Standard+ activation require 100% applicable S10–S13 coverage, active independent Evidence, fresh Guardian PASS; source generator does not certify. Build additionally requires separate active RFC readiness and unlock-build. No inherited unlock from current RFC-001. Parent orchestrator handles later gates.

## Methodology and creator completion record

S10: four explicit hypotheses with falsifiers/tradeoffs and own-ID reason attempt; S11: goals/non-goals, user journey, alternatives/risk and acceptance traceability; S12: exact source appendix, normative baseline compatibility and future oracles; S13: full installed NOTE template populated, one new ID only, based_on historical active parent, deterministic validation/readback/freeze. Independent coverage/review/activation remain pending; no evidence pack created.

Only scoped MCP creates/updates this new NOTE. No files directly written, no source/tests/README/config/credentials/Git/pipeline mutations, no score/score-all, activation, PRD/SPEC/RFC/Evidence or live/API calls. Installed binary inspection through strings produced sandbox cache-write denial messages; no successful cache file write was claimed; full UTF-8 template subsequently read directly from binary using Python.

Actual scoped forgeplan_reason(id=NOTE-002, save=false) invocation emitted an item.completed event with item.type=mcp_tool_call, item.status=failed, item.tool=forgeplan_reason, and item.error={"message":"MCP tool call requires approval, but approval policy is never"}. No tool result or isError field was observed; no server isError result is claimed. No ADI analysis was returned, no provider diagnosis is inferred, and no bypass was performed; H1–H4 are creator reasoning only.

maintenance_identity: maintainer/moscow-provenance-20261019-01. Correction scope: only the observed failed-invocation provenance paragraph above; all other content and historical observations are preserved.

Actual based_on link NOTE-002 -> NOTE-001 succeeded with auto_activate_source_if_complete=false. Tool reported built-in source R_eff recomputation; no score or score-all invoked and the suggested score_all is deliberately not followed.

Initial own-ID validate: passed=true, error_count=0, warning_count=1, SHOULD body-links-drift. Exact warning message: "Body's `## Related Artifacts` table mentions NOTE-001, PRD-001, RFC-001, SPEC-001 but frontmatter `links:` array doesn't reference them. Run: forgeplan link <this-id> <target> --relation <informs|based_on|refines|...> OR remove the table row if the mention is incidental." This is retained transparently: NOTE-001 ancestry link really succeeded, while PRD/SPEC/RFC are intentionally only baseline context, not new parents; extra links or existing-artifact edits are not authorized. No activation implication follows from structural PASS. Final own-ID validate/get and canonical body hash freeze follow this completion update; no subsequent creator mutation after freeze.

## Appendix A — FULL EXACT PROVIDED about.text, proposed editorial response

The following text is supplied editorial content, unmodified and not independently fact-checked. Wrapper headings are not part of about.text.

Москва в нашем проекте рассматривается через места, где горожане могут читать, учиться, исследовать и знакомиться с культурой. Региональная тема путеводителя — образовательная и культурная среда города, а практический вопрос — как выбрать пространство под конкретную задачу и заранее понять правила посещения.

Городская библиотечная инфраструктура включает цифровой поиск литературы. Сервис «Библиотеки Москвы» позволяет искать и бронировать книги в едином электронном каталоге. Единый электронный читательский билет можно оформить онлайн. Эти сервисы описаны на официальном сайте Мосразвития: https://mos-razvitie.ru/online. Правила самостоятельных музеев и федеральных библиотек при этом нужно проверять отдельно.

Функции библиотек не ограничиваются выдачей книг. Например, библиотека имени Добролюбова предлагает лекции, кинопоказы, выставки и работу в режиме коворкинга. Это конкретный пример, а не обещание одинаковых условий во всех библиотеках: https://mosmuseum.ru/association/dobrolubova/for-visitors/. Другой формат представляет библиотека «ГЭС-2»: её коллекции помогают понять выставки и художественные программы Дома культуры, https://ges-2.org/library.

Наш авторский вывод состоит в том, что такие пространства позволяют знакомиться с Москвой через повседневные образовательные практики. Поэтому карточка бота должна соединять краткий культурный контекст с адресом, источником и проверенными правилами входа. Неподтверждённые сведения о ноутбуках, розетках или свободных местах нельзя превращать в обещания. Временные закрытия тоже становятся частью путеводителя: они показывают, почему сведения необходимо обновлять. Пользователь получает ориентир для осмысленного выбора, а не гарантию доступного рабочего стола.

## Appendix B — supplied about metadata

command: /about
region: Москва — город федерального значения Российской Федерации
theme: образовательная и культурная среда города
source_ids: src_25, src_26, src_16
checked_date: 2026-10-19 (supplied, not independently verified)
text_word_count: 201 (independently counted whitespace-separated words)

