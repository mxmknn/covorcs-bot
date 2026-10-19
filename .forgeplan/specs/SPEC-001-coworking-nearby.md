---
depth: standard
id: SPEC-001
kind: spec
last_modified_at: 2026-10-18T19:44:40.301271+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-001
  relation: based_on
status: active
title: Coworking Nearby — строгий локальный контракт каталога
---

# SPEC-001: Coworking Nearby — строгий локальный контракт каталога

## Summary

Локальный контракт UTF-8 JSON каталога владельца: один объект описывает один конкретный филиал, общий строгий валидатор атомарно возвращает нормализованный список либо понятную ошибку до polling.

generator_identity: creator/catalog-spec-20261018-01
generator_role: creator
depth: standard
status: draft
type: Data Model / Local Protocol
parent: NOTE-001
parent_revision: 2026-10-18T18:29:58.718062+00:00
source_version: 1.0 от 18.10.2026
source_path: /Users/mxmknn/.codex/attachments/38a9bdff-7b37-4c55-8851-d338dfe1c340/Pasted text.txt

## Scope

C01–C08 ниже описывают только локальную загрузку, модель, нормализацию, инварианты и диагностику. Нормативная база — весь оригинал §1–15 и active NOTE-001, прочитанные целиком; приложение Brief не заменяло чтение оригинала. Источник §15 содержит собственное заявление о документации; внешние документы этим creator не проверялись.

Прочитаны AGENTS.md, creator TOML, config.yaml, pipeline.py, pipeline.json, PARENT_RULES и installed Standard SPEC через new/get. В видимом дереве приложения пока нет, находятся инструкции и служебные файлы. Health=needs_attention: общие advisory/orphan замечания не являются gate этого SPEC; другие planning artifacts не читались и не изменялись. Pipeline phase=prd, route=1, standard, dev_unlocked=false; пользователь уже одобрил Row1 BMAD+SpecKit Standard cycle и PRD stage. Разработка не запускается.

Не входят: маршрутные URL FR-07/AC-07–08, Haversine, ranking/ties, округление расстояний, renderer, Telegram runtime/concurrency/retry/privacy implementation. Их связи с исходником сохраняются, решения и интеграционные проверки принадлежат будущему RFC. Никаких сетевых страниц, API, HTTP-сервера, scraping, геокодера или извлечения координат из URL/адреса.

## Hypotheses

### Hypothesis H1 — do-nothing
Оставить контракт только в исходнике. Нет нового расхождения документов, но неоднозначности URL/нормализации остаются и поручение создать SPEC не исполнено. Отклонена.

### Hypothesis H2 — scope-reduction
Описать лишь id/name/address/coordinates. Меньше контракт, но optional defaults, источник рейтинга и atomic failure не согласованы; FR-08 и AC-10/11/14 неполны. Отклонена.

### Hypothesis H3 — Hselected narrow strict shared local contract
Один локальный JSON и общий startup/offline validator дают одну семантику принятия/отказа. Выбрана по §4/9/11 и поручению, а не по измеренным результатам. Tradeoffs: единичная ошибка блокирует весь файл, узкая URL policy отклоняет часть потенциально полезных ссылок, semantic acceptance остаётся владельцу; зато нет тихой потери записей и сетевой зависимости.

### Hypothesis H4 — расширение
Автогеокодинг, live ratings, API enrichment и permissive parsing могут упростить импорт, но добавляют зависимости, искажения и несанкционированный scope. Отклонена для этого контракта.

Дедукция: H1 не создаёт требуемый результат, H2 теряет AC, H4 нарушает границы, H3 покрывает локальный контракт с явными tradeoffs. Индукция ограничена исходником: полезность реального каталога ещё не доказана. Недоказанные metrics/results, product SLA, тестовые PASS и фактическая реализация запрещены; измеренных результатов нет.

## API Contracts

### Local load/check contract — C01

Input: явно выбранный локальный путь CATALOG_PATH, default data/coworkings.json, и его bytes. Прочитать весь файл строгим UTF-8, затем JSON top-level array объектов. PROPOSAL: UTF-8 BOM и unpaired surrogate code points отвергать как encoding/JSON input ambiguity; повторяющиеся ключи объекта отвергать, не применять last-wins.

Output success: полный ordered normalized list Coworking в порядке файла, включая active=false. Никакого HTTP endpoint/status/event bus. Семантический тип результата — success(list) либо failure(diagnostic), без частичного списка. Имена функций и точное имя standalone-команды выбирает RFC; исходное load_catalog(path) — ориентир, не реализованный API.

C02: один и тот же валидатор используется будущими bot startup и standalone offline check: идентичные accept/reject, normalization и diagnostic class для одного файла. Offline check не требует BOT_TOKEN и не подключается к Telegram/HTTP/Яндексу. Успех, включая [], даёт успешное завершение standalone; failure — неуспешное. Числовые exit codes определит RFC.

Startup не переходит к polling до полного success. При первом обнаруженном дефекте fail fast, весь файл отклоняется; требование «целиком» означает отсутствие принятого частичного каталога, не обязанность собрать все ошибки. Невалидные inactive записи не пропускаются.

### Diagnostics — C03

Диагностика содержит path, class, field и normalized id когда доступен, иначе zero-based index. Для file/encoding/JSON/root дефектов запись ещё неизвестна: index/id=N/A, field=$file/$encoding/$json/$root; для неизвестного поля указать его точное имя. Для JSON syntax допустимы line/column. Не печатать весь файл. Точные wording/code symbols закрепит RFC, перечисленные классы являются общим контрактом.

| Class | Field/context | Meaning/action |
|---|---|---|
| configuration/file | $file, path | missing/unreadable file; объяснить проверить CATALOG_PATH, наличие и права; demo не подставлять |
| encoding | $encoding, path | unreadable UTF-8/BOM policy |
| JSON | $json, path | invalid syntax, nonstandard NaN/Infinity, duplicate member, invalid Unicode |
| root | $root | root не array |
| entry | index | element не object |
| unknown_field | exact field, id/index | поле вне closed model |
| required/type/length | field, id/index | missing/null/blank required, неверный тип или длина |
| duplicate_id | id и index конфликтующей записи | normalized id уже встречался |
| number/range | latitude/longitude | запрещённый numeric type, nonfinite или вне bounds |
| date | date field | неверный формат/невозможный календарный день |
| URL | yandex_maps_url | нарушение C06 |
| conditional | rating_checked_at или yandex_maps_url, id/index | yandex rating_text без требуемого значения |

Порядок выбора первой ошибки среди нескольких не является внешним oracle; обе точки входа обязаны использовать один алгоритм. Ошибка в последней записи не разрешает использовать предыдущие.

## Data Models

### Entity: Coworking — C04

Closed object: только перечисленные 13 полей, case-sensitive имена. Required не имеют defaults. JSON integer/fraction/exponent — numbers, если конечны и в диапазоне; numeric strings, boolean, null не numbers. Не приводить типы.

PROPOSAL normalization pending SPEC approval: trim внешних символов из фиксированного набора U+0009–000D, U+0020, U+0085, U+00A0, U+1680, U+2000–200A, U+2028–2029, U+202F, U+205F, U+3000 для всех string fields. Length считается после trim в Unicode code points, не bytes/UTF-16/graphemes. Никаких case folding, NFC/NFKC, collapse внутренних пробелов, HTML escaping или переписывания текста. Unicode scalar content сохраняется точно помимо trim. Пустая строка означает length=0 после trim.

missing в normalized model — отсутствие ключа для nullable optional fields. Для обязательных/defaulted ключи присутствуют. Входной null принимается только для nullable полей из таблицы.

| Field | Strict input type | Required/omitted/default | Null/blank | Constraints and normalized output |
|---|---|---|---|---|
| id | string | required | invalid/invalid | 1–64 code points; trim; case-sensitive unique normalized id во всём файле |
| name | string | required | invalid/invalid | 1–150 code points; trim |
| address | string | required | invalid/invalid | 1–250 code points; trim; semantic obligation C05 |
| latitude | JSON number | required | invalid; string invalid | finite [-90,90], inclusive; zero valid; сохранить numeric value |
| longitude | JSON number | required | invalid; string invalid | finite [-180,180], inclusive; zero valid |
| active | boolean | omitted becomes true | null invalid; любые strings, включая blank, invalid | только true/false, без coercion; false сохраняется |
| yandex_maps_url | string or null | omitted missing | null/blank become missing | nonblank trim, C06; дополнительного URL length limit нет |
| short_review | string or null | omitted missing | null/blank become missing | max 200 code points; one/two phrases — редакционная обязанность владельца, не sentence regex |
| description | string or null | omitted missing | null/blank become missing | max 500 code points |
| rating_text | string or null | omitted missing | null/blank become missing | max 50 code points; текст, не numeric scale |
| rating_source | string | omitted becomes catalog | null invalid; blank becomes catalog | after trim exact enum catalog/yandex, case-sensitive |
| rating_checked_at | string or null | omitted missing | null/blank become missing | C07 YYYY-MM-DD |
| updated_at | string or null | omitted missing | null/blank become missing | C07 YYYY-MM-DD, дата записи не metadata SPEC |

Все optional string values с blank после trim считаются absent; для rating_source затем применяется default catalog. active не string field: blank не делает его absent. Для остальных optional полей числа/boolean/array/object invalid; для rating_source также null invalid. Для required strings non-string invalid; для coordinates omitted/null invalid.

C05: филиал/название/адрес с городом и номером дома/координаты/предоставленная ссылка должны описывать одно место (§4/7/14). Это OWNER data acceptance obligation. Validator синтаксически проверяет address лишь как непустую строку в лимите; geocoder и brittle city-house regex запрещены. Synthetic address «Москва, тестовый адрес» из исходника иллюстративен, не доказывает semantic acceptance и существование реального коворкинга. Две записи разных id с одинаковыми координатами valid; id не генерируется из coords.

### URL policy — C06 (PROPOSAL pending SPEC approval)

Исходник требует HTTPS и explicit allowlist, но не задаёт окончательный список/синтаксис. Этот проектный narrow proposal не является полным официальным списком доменов и не подтверждает содержимое страницы.

После общего trim URL должен быть абсолютным syntactically parsed URL с явным authority и scheme HTTPS; scheme и host сравниваются ASCII case-insensitive. Hosts только exact yandex.ru и yandex.com. Wildcard subdomains, www, trailing dot, encoded host, IDN lookalikes, IP literals, пустой host, userinfo (даже empty) запрещены. Authority допустим только ASCII host из allowlist без порта либо с literal :443; :0443, пустой port, другой/нечисловой port запрещены. Схему/host не переписывать в output: проверка insensitive, сохранённый URL точно после trim.

Raw path case-sensitive: exactly /maps либо начинается /maps/. Пустой path, /mapsx, /MAPS, /map, /%6Daps, //maps запрещены. PROPOSAL: внутри path запрещены percent-encoded slash/backslash, dot segments . или .. включая percent-encoded dots; сравнение prefix без percent-decoding, никакой неявной path normalization. Query/fragment допустимы как данные, координаты из них не извлекаются.

После trim нигде не допускаются raw Unicode whitespace из trim-набора, ASCII C0 controls/U+007F, backslash. Каждый % должен иметь два ASCII hex digits; encoded C0/DEL/backslash запрещены во всех компонентах. Синтаксически невалидные authority/brackets/port/percent sequences отклонять, не «исправлять» браузерным parsing. Обычное percent-encoding данных в path/query/fragment допускается, если не нарушает перечисленные запреты. URL синтаксическая проверка не удостоверяет реальный филиал.

Не fetch redirects/pages, не API, не resolve shortlinks. https://yandex.ru/maps/-/synthetic синтаксически допустим; его существование/назначение не доказано. https://ya.ru/abc, https://yandex.ru/-/abc, https://yandex.com/navi/abc отклоняются. Поддержка произвольных коротких ссылок не обещана. Карточка организации отдельно от будущих route links.

### Dates and ratings — C07/C08

C07: после trim ровно ASCII YYYY-MM-DD, четыре цифры года 0001–9999, фактический Gregorian calendar. Leap rule: divisible by 4, except centuries unless divisible by 400. 2024-02-29 valid, 2025-02-29 и 1900-02-29 invalid, 2000-02-29 valid. Невозможные даты, timestamp, неzero-padded поля invalid. Никаких freshness/future restrictions, сравнения updated_at с rating_checked_at или today не вводится.

C08: только если normalized rating_text present и rating_source=yandex, требовать present valid yandex_maps_url и rating_checked_at. Null/blank обоих зависимых полей не выполняют условие. Все present поля валидируются независимо от условия. yandex без rating_text допускается без URL/date; отсутствующий/пустой рейтинг остаётся отсутствующим, никакого нуля/звёзд/придуманной шкалы. catalog rating не Яндекс, значение «8/10», «4,7/5» или текст не преобразуется. source §3/AC-11: future renderer отображает дату рейтинга ДД.ММ.ГГГГ и источник сохранённого рейтинга; этот SPEC предоставляет данные, renderer implementation решает RFC.

## Relationships

Local file contains ordered zero-or-more Coworking; одна запись один конкретный филиал. id уникален в пределах одного каталога. Реляционной БД, tenant/entity foreign keys и внешних lookup нет. Normalized list содержит inactive, future consumer исключает active=false перед подбором (§5 FR-06). Validator не вычисляет distance/ranking/route origin.

SPEC-001 based_on NOTE-001 active Standard указанной ревизии; PARENT_RULES допускает active NOTE для spec. Существующий параллельный PRD не читается, его ID не указывается, связь с ним не создаётся. Никакие старые artifacts не обслуживаются.

## Validation Rules

C01–C08 совместно образуют контракт. Fail-fast all-or-nothing распространяется на inactive и все optional present fields. Никакого silent skip/coercion/partial catalog, автозагрузки demo и сетевого fallback. Все defaults применяются только как определено таблицей. Working real catalog [] valid, missing file configuration error; owner обновляет файл и перезапускает процесс, hot reload вне scope.

### Future GIVEN/WHEN/THEN oracle

Все строки — будущие обязательства проверки, не выполненные тесты. Base B — синтетический объект id=demo-001, name=ДЕМО, address=Тестовый город, ул. Пример, д. 1, latitude=0, longitude=0; это не сведения о реальном месте. Для ошибок oracle проверяет failure class/path/field/id-or-index и отсутствие принятого списка; обе точки входа одинаковы.

| Scenario/source | GIVEN | WHEN | THEN future oracle |
|---|---|---|---|
| T01 §4 AC-14 | valid B | load | success; active=true, rating_source=catalog, nullable optional keys absent |
| T02 §4 AC-14 | каждый из id/name/address отсутствует, null, empty, trim-only или non-string | load каждый variant | required/type failure соответствующего поля; index=0 если id недоступен |
| T03 §4 AC-14 | id 64/name150/address250/short_review200/description500/rating_text50 code points | load exact limits затем limit+1 отдельно | limits success, overlimits length failure; trim до length, astral symbol один code point |
| T04 §4 AC-14 | nullable optional поля по одному omitted/null/empty/trim-only | normalize | все missing; rating_source omitted/blank становится catalog, null invalid |
| T05 §4 AC-14 | каждое optional поле имеет wrong type: number/bool/array/object; active дополнительно null/empty/string true/0/1 | load variants | type failure; only active true/false accepted, omitted true; rating_source Catalog/YANDEX invalid |
| T06 §4 AC-13/14 | latitude -90/90 и longitude -180/180, zeros и negative fractions | load | success; за пределами границ по отдельности range failure |
| T07 §4 AC-14 | coordinates numeric strings/bools/null/omitted, JSON NaN/Infinity/-Infinity или overflow nonfinite | load | type/JSON/number failure, никогда accepted number |
| T08 FR-06 AC-06/13 | два разных id при same coords, включая zeros | load | две записи success; future consumer zero distance/ties отдельно в RFC |
| T09 §4 AC-14 | ids " a " и "a"; либо "a" и "A" | normalize | первая пара duplicate_id; вторая success case-sensitive; unknown field/name case typo failure |
| T10 §4 AC-14 | dates 2024-02-29,2000-02-29,0001-01-01,9999-12-31; future date | load | valid success без проверки freshness |
| T11 §4 AC-14 | 1900-02-29,2025-02-29,2026-04-31,0000-01-01,2026-2-01,timestamp, nonstring | load | date/type failure; omitted/null/blank dates missing |
| T12 §4 AC-11/14 | https://yandex.ru/maps, https://yandex.com/maps/org/demo, HTTPS://YANDEX.RU:443/maps/?q=a%20b#x | validate C06 | syntactic success; owner ещё подтверждает место; URL не fetch |
| T13 §4 AC-11/14 | http/javascript/relative URL; evil host, sub.yandex.ru, yandex.ru.evil, user@yandex.ru, yandex.ru@evil, yandex.ru., encoded host, malformed bracket | validate | URL failure, authority не исправляется |
| T14 §4 AC-14 | URL с :80/:0443/:/nonnumeric port, /mapsx,/MAPS,empty path,/%6Daps,//maps,/maps/../x,/maps/%2e%2e/x,encoded slash | validate | URL failure; omitted port и :443 accepted |
| T15 §4 AC-14 | interior raw space/control/backslash, malformed %/%G0, encoded control/backslash | validate | URL failure; trim exterior whitespace permitted |
| T16 §4 AC-11 | syntactic maps/-/synthetic versus ya.ru/abc, yandex.ru/-/abc, yandex.com/navi/abc | validate | first accepted syntactically без resolve, остальные rejected; arbitrary shortlink support отсутствует |
| T17 FR-08 AC-10/11 | rating_text present+yandex, URL/date по одному omitted/null/blank или invalid | load | conditional либо URL/date failure; обе valid дают success |
| T18 FR-08 AC-10/11 | catalog rating, default catalog, no/blank/null rating_text; yandex без rating | load | no rating invented; source exact; no dependency если rating absent, но invalid present URL/date всё равно reject |
| T19 FR-03/06 AC-05/12 | [], [B], две valid записи, только active=false | load | success 0/1/2/full inactive list; future selection 0/1/2/0 без duplicates — интеграционный oracle RFC |
| T20 FR-06 AC-14 | inactive B с bad date/type/unknown field | load | whole-file failure до polling, active=false не оправдывает пропуск |
| T21 AC-14 | missing/unreadable file, invalid UTF-8/BOM, broken JSON, root object/null, entry string/null, duplicate JSON member | load each | file/encoding/JSON/root/entry failure с path и field, index где применимо |
| T22 AC-14 | valid first record и invalid last | startup/offline | одинаковый failure class, ни partial list, ни polling; offline без token/network |
| T23 FR-08 AC-10/15 | texts содержат &, angle brackets, single/double quotes, внутренние пробелы | normalize | точное сохранение помимо outer trim; future renderer escaping проверяется отдельно, AC-15 сейчас не tested |
| T24 §4/7/14 | syntactically valid address без house / URL с ll без coords | load и owner acceptance | address syntax success не semantic approval; missing coords failure, ll/address не заменяют named fields |

### Traceability and owned responsibilities

| SPEC | Source FR/AC | Owned obligation | Deferred integration/owner |
|---|---|---|---|
| C01–C03 | §4/9 FR-03/06 AC-12/14 | atomic local input/output/errors; shared validator | RFC startup before polling и standalone wiring, future verifier |
| C04/C05 | §4/7 FR-06 AC-05/06/13/14 | strict fields, defaults, id, numeric/samecoords rules | owner реальность филиала/город+дом; RFC selection/ranking/ties/distant origin |
| C06 | §4 FR-08 AC-11/14 | syntactic HTTPS proposal, no network/coordinate extraction | owner link-place correspondence; RFC route URLs FR-07 AC-07/08 |
| C07/C08 | §3/4/7 FR-08 AC-10/11 | dates, source, missing rating, conditional error | RFC renderer source labels, date ДД.ММ.ГГГГ, no invented ratings |
| C04/C08 | §3 FR-03/08 AC-10/15 | exact data beyond trim, length constraints | RFC escaped HTML/card assembly/fallbacks and Telegram size; no added URL length cap |

AC-05 active filtering, AC-06 sort/ties, AC-13 user origin/distance, AC-15 rendering требуют интеграционных проверок за пределами validator. Каталог не доказывает всю продуктовую приёмку. Никакой неподтверждённой гарантии Telegram message size: URL без дополнительного лимита и escaping следует отдельно разобрать в RFC без скрытого изменения этого контракта.

## Events / Side Effects

| Trigger | Observable outcome | Responsibility |
|---|---|---|
| Owner edits local file/restarts | complete reload or diagnostic | future loader/startup; source §4 |
| Valid file, including [] | normalized list only; no external events/network | shared validator |
| Invalid file | failure, no accepted partial list, startup blocked before polling | shared validator/startup |
| Offline check | success/failure without BOT_TOKEN/HTTP/Telegram | future standalone adapter |
| Consumer uses list | ignores inactive for search | future RFC; validator retains inactive |

Чтение каталога не меняет файл и не создаёт places. Synthetic demo хранится отдельно с явной маркировкой, никогда автоматически вместо real data/coworkings.json. Пока owner не предоставил реальные записи, real catalog остаётся []; текущий creator файлов не создаёт.

## Versioning

| Version | Date | Changes |
|---|---|---|
| 1.0 proposed draft | 2026-10-18 | Первый контракт на базе original v1.0 и active NOTE-001; normalization/URL policies — явные proposals |

Никаких существующих контрактов не supersedes. Будущие изменения полей/defaults/acceptance проходят отдельное решение и version review; silently accepting unknown fields запрещено. Текущая версия не активирована, изменение source schema при одобрении не подразумевает миграцию реальных данных без владельца.

## Related

- NOTE-001: active Standard Brief; based_on, exact parent revision указан выше.
- Original v1.0: полный source_path выше, §4 основной контракт, §3/7 происхождение данных, §10 AC, §12/14 real/demo.
- Будущий RFC: implementation, command name, startup adapter и integration tests; ID не назначается этим creator.

## Standard methodology applicable layers S10–S13

| Layer | Draft coverage / obligation | Gate state |
|---|---|---|
| S10 FPF ADI | H1–H4, deduction/tradeoffs, Hselected; real forgeplan_reason attempt save=false после body | Independent active ADI Evidence отсутствует для этого draft; не substitute собственными гипотезами, pending |
| S11 BMAD review | source FR/AC traces, risks, owner responsibilities, future GIVEN/WHEN/THEN oracle | Независимый reviewer по frozen revision и active review Evidence требуются отдельно; не выполняются creator |
| S12 OpenSpec | inputs/output/invariants/errors C01–C08, scenarios, based_on active NOTE допустим PARENT_RULES | link создаётся после body, без autoactivation; не заявляется полный gate |
| S13 ForgePlan | installed template sections заполнены, new ID only, final validate/get и freeze revision | фактический validation отдельно; activation запрещена |

Применимы все S10–S13, ни один не объявлен N/A. 100% applicable coverage, active independent Evidence и fresh Guardian PASS для Standard activation ещё не доказаны. Creator не сертифицирует gate, Evidence не создаёт, status остаётся draft и development blocked.

## Unresolved assumptions, risks and limitations

1. OWNER должен предоставить/проверить реальные записи и semantic city+house/one-place соответствие; schema success не доказывает качество. Working [] valid; полезность не измерена.
2. Предлагаемые trim set/code-point length, required-string trim/normalized id uniqueness, URL allowlist/syntax/port и strict JSON ambiguity policies требуют SPEC approval. Allowlist narrow, не официальный полный список; reachability не проверяется.
3. RFC должен определить точное имя offline command, language representations/errors ordering/exit codes, startup wiring, ranking/routes/renderer/Telegram message assembly без изменения принятого schema. No source/test writes до законного unlock-build.
4. BOT_TOKEN нужен только будущему live запуску, не offline catalog check. Реальных ключей/запросов и synthetic code/tests сейчас нет.
5. Проверки таблицы планируются, не запускались; measured results/product metrics отсутствуют. Независимые review/ADI/Guardian и gate pending.
6. Реальный scoped role вызов forgeplan_reason id=SPEC-001 save=false вернул isError=true и точный текст: "MCP tool call requires approval, but approval policy is never". Runtime approvalnever запретил вызов; обход не предпринимался, reasoning output не получен и не имитируется. Отсутствие provider не диагностировано. Собственные H1–H4 не являются независимым ADI.








