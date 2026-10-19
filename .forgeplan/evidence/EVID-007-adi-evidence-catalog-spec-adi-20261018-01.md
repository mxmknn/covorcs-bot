---
depth: tactical
id: EVID-007
kind: evidence
last_modified_at: 2026-10-18T19:53:08.170150+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: SPEC-001
  relation: informs
status: active
title: Независимый ADI локального каталога — evidence/catalog-spec-adi-20261018-01
---

# EVID-007: Независимый ADI локального каталога

| Field | Value |
|-------|-------|
| Status | Draft |
| Created | 2026-10-18 |
| Valid Until | Не задано в metadata; применимо только к точному pin ниже |
| Target | SPEC-001 |

## Structured Fields

evidence_type: measurement
verdict: supports
congruence_level: 3
reviewer_identity: evidence/catalog-spec-adi-20261018-01
reviewer_role: evidence-gatherer
generator_identity: creator/catalog-spec-20261018-01
target_id: SPEC-001
target_updated_at: 2026-10-18T19:44:40.337539+00:00
target_body_sha256: 624c779e261def14b7fa56ed477b82e7b0b8b581acb7ff5a2c92bcedb7aa78b8

## Measurement

Объект измерения — полнота и логическая согласованность текста контракта, не скорость, спрос или работоспособность программы. Независимо прочитаны AGENTS.md, .codex/agents/forgeplan-evidence-gatherer.toml, весь фактический SPEC-001 (24272 символа body), весь active NOTE-001 и отдельно весь оригинал v1.0 от 18.10.2026 по пути /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt. Другие review Evidence и PRD не читались.

Начальный pin совпал; based_on NOTE-001 подтверждён проекцией, родитель active/standard updated_at=2026-10-18T18:29:58.718062+00:00. Health healthy с advisory, не gate PASS.

Реально вызван scoped forgeplan_reason({id:"SPEC-001",save:false}). Точный видимый результат: {"content":[{"type":"text","text":"MCP tool call requires approval, but approval policy is never"}],"isError":true}. Автоматический ADI не выполнен: запрет approval; provider не диагностирован. Creator сохраняет тот же error; isError вместо transport status=failed не было бы существенным искажением. Ниже — собственное независимое рассуждение роли, не tool output. 

## Result

Сопоставлены все 13 полей C04 и 24 будущих GWT T01–T24. Документально поддерживается строгое общее SHARED поведение startup/offline по §4,9,11 исходника. Verdict supports относится к проектному локальному контракту при сохранении явно предлагаемых политик до одобрения. Это не удостоверение реализации, прохождения тестов или готовности активации.

### Hypothesis A — единица доверия есть весь снимок каталога

Абдукция: главный источник расхождений может быть не отдельная ошибка типа, а разные правила доверия между загрузкой для бота и автономной проверкой. Если обе точки входа используют один строгий контракт всего снимка, отрицательный результат становится воспроизводимым без сети.
Дедукция: файл принимается полностью либо не даёт списка; inactive остаётся в normalized list и тоже проверяется, поскольку завтра владелец может активировать её. Ошибка последней записи блокирует polling; диагностике нужны path, class, field и id/index. Fail-fast не требует собрать все ошибки. Отклонение unknown fields выявляет опечатку, а не silently теряет данные.
Evidence: исходник прямо требует целостную проверку, общий валидатор и отсутствие незаметно испорченного каталога; C01–C03/T20–22 согласованы с этим. Фальсификатор: независимые accept/reject правила offline и startup либо принятие valid prefix опровергнут гипотезу при будущей реализации.
Tradeoff: одна неактивная ошибочная запись мешает запуску всего списка и увеличивает редакционную работу. Сохранение корректного снимка важнее частичной выдачи по данному исходнику, но эксплуатационная цена не измерена. Выбрана эта гипотеза.

### Hypothesis B — permissive partial/coercive parser
Абдукция: пропуск bad/inactive rows, coercion "55"/true и игнорирование unknown keys могли бы облегчить импорт. Дедукция: состав списка станет зависеть от неявных преобразований; offline success уже не означает пригодность файла. Фальсификация: §4/AC-14 явно отвергают неверные типы, bool/nonfinite, unknown fields и повреждённый каталог. Tradeoff — меньше исправлений ценой недостоверной выдачи; отвергнута. Возврат требует отдельного изменения требований, спрос на терпимость не установлен.

### Hypothesis C — do-nothing / scope-reduction
Абдукция: без реальных записей можно оставить только оригинал или пять required полей. Дедукция: это экономит согласование, но оставляет разные defaults/null/атрибуцию и offline semantics. Evidence/фальсификация: §4 перечисляет все optional поля, §11 требует контракт, AC-10/11 зависят от них. Поэтому сокращения недостаточно для поручения. Tradeoff — меньший объём сейчас против будущего расхождения; обе альтернативы отклонены без заявления об окупаемости.

### Hypothesis D — remote enrichment
Абдукция: удалённое разрешение адреса/URL могло бы уменьшить ручную сверку. Дедукция: появляется другой источник доверия, сетевые отказы и условия доступа; ll может быть центром карты, доступная страница не доказывает филиал. Evidence/фальсификация: §1/7/13/14 требуют каталог владельца, без API обычного поиска; наполнение отдельное. Оригинал не требует геокодинга/API. Tradeoff — возможная экономия редактора против недоказанных данных и расширения scope. Отклонена для MVP; semantic acceptance у владельца.

## Interpretation

Выбрана A по критерию воспроизводимого снимка доверия. Полнота схемы:

- id/name/address: required strings без defaults; missing/null/blank/nonstring отказ, длины после предлагаемого trim 1–64/150/250. id unique после нормализации во всём файле, case-sensitive; " a " и "a" конфликтуют, "a" и "A" различны. Одинаковые coordinates при разных id допустимы.
- latitude/longitude: required JSON numbers без defaults, конечные и в включённых пределах ±90/±180. Ноль и отрицательные дроби допустимы; bool, strings, missing/null, NaN/Infinity и overflow nonfinite отвергаются. Проверка numeric value не должна наследовать bool-as-int языка.
- active: только boolean, missing=true, false сохраняется; null/blank/"true"/0/1 отказ. Фильтрация active — будущий consumer, не валидатор.
- yandex_maps_url: nullable optional string; omitted/null/trim-blank становятся missing; nonblank проверяется локальным разбором C06, wrong types отказ. URL не загружается, ll не заменяет named coordinates.
- short_review/description/rating_text: nullable optional strings; omitted/null/blank missing, максимум 200/500/50 code points. Рейтинг остаётся текстом, "8/10" не превращается в число; 1–2 фразы — редакционная обязанность, не sentence regex.
- rating_source: omitted/blank даёт catalog, null/wrong type отказ; enum catalog/yandex case-sensitive. Дефолт не доказывает происхождение неизвестного рейтинга и не разрешает называть его Яндексом.
- rating_checked_at/updated_at: nullable optional strings; missing/null/blank отсутствуют, present строго ASCII YYYY-MM-DD и Gregorian 0001–9999. Leap century rules заданы; timestamp/невозможные даты отказ. Свежесть, запрет будущей даты и порядок двух дат не добавляются.

При present rating_text+yandex обязательны valid present URL/date; null/blank условие не выполняют. При yandex без текста условие не срабатывает, но любое заполненное поле всё равно валидируется. Whole-file rejection, включая inactive, не ослабляется optional статусом поля.

URL policy exact yandex.ru/yandex.com и /maps или /maps/, :443, запреты userinfo/subdomains/trailing dot/encoded ambiguity — PROPOSAL pending approval, не факт оригинала и не официальный полный allowlist. Полезные www/региональные/короткие ссылки, иные пути или браузерно нормализуемые варианты могут быть false negatives. Владелец должен заменить ссылку на разрешённую или отдельно согласовать расширение, а не ожидать resolve redirects. Query/fragment только данные; синтаксический success synthetic URL не подтверждает ни существование страницы, ни филиал. Доля false negatives неизвестна.

Trim fixed Unicode set, code-point length, отсутствие NFC/NFKC/case folding, rejection BOM/unpaired surrogates/duplicate keys также PROPOSAL. Они ограничивают скрытую неоднозначность: last-wins не прячет повторный active/id. Цена — отказ редакторского UTF-8 с BOM, визуально одинаковые Unicode id могут остаться разными, широкие пробелы по краям удаляются. Эти решения не выданы за дословное требование источника; фальсификатор их пригодности — реальные редакторские файлы после предоставления владельцем, сейчас таких наблюдений нет.

Address syntax success не подтверждает город/дом и согласованность названия/ссылки/координат одного филиала; владелец обязан сверить их. Рабочий real [] валиден, missing file ошибочен; отдельный маркированный synthetic пример не подставляется автоматически. Иллюстрация «Москва, тестовый адрес» не является принятой реальной записью.

24 GWT рассмотрены как будущие oracles: T01 defaults; T02 required; T03 границы длины; T04 missing/null/blank; T05 типы/enum; T06 numeric bounds; T07 nonfinite/bool/string; T08 same coordinates; T09 normalized id/unknown keys; T10 valid dates; T11 invalid dates; T12 positive URL; T13 authority/scheme; T14 port/path; T15 controls/percent; T16 narrow shortlink policy; T17 conditional yandex; T18 no invented rating; T19 []/1/2/inactive; T20 invalid inactive; T21 file/encoding/JSON/root/entry; T22 atomic shared failure; T23 text preservation; T24 semantic owner boundary. Все они будущие, не выполненные тесты. T19/T23/T24 содержат отложенные consumer/renderer/owner обязательства; loader success не удостоверяет AC-05/06/13/15 целиком. Точное имя команды, startup wiring, exit codes, escaping и итоговый размер Telegram карточки остаются RFC. URL без лимита длины не доказывает вместимость карточки.

## Congruence Level Justification

CL3: прямое сопоставление точного локального target с его active parent и оригиналом в том же контексте. Это уровень соответствия контекста, не уверенность в реализации. Разработка, source/tests, live вызовы и проверка §15 не выполнялись. Автоматический ADI unavailable; самостоятельный ADI выше имеет документальную основу и ограниченный verdict supports. Независимая artifact-reviewer оценка и Guardian принадлежат другим ролям; Standard activation и S10–S13 gate этим Evidence не сертифицируются. Активация остаётся pending user approval.

## Related Artifacts

SPEC-001: informs, автоматически через parent_id; связь подтверждена в проекции.



