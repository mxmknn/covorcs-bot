---
depth: deep
id: NOTE-003
kind: note
last_modified_at: 2026-10-19T11:09:00.958419+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: PRD-001
  relation: based_on
- target: SPEC-001
  relation: based_on
- target: ADR-001
  relation: based_on
- target: RFC-001
  relation: based_on
status: active
title: Brief — предложения мест, модерация и реестр пользователей — Deep
---

---
id: NOTE-003
kind: note
status: draft
depth: deep
methodology: sparc
architecture: hexagonal
route: "3"
generator_identity: creator/places-brief-20261019-01
generator_role: forgeplan_creator
label: brief-intake
labels: [brief-intake]
created: 2026-10-19
updated: 2026-10-19
links:
  - target: PRD-001
    relation: based_on
  - target: SPEC-001
    relation: based_on
  - target: ADR-001
    relation: based_on
  - target: RFC-001
    relation: based_on
---

# NOTE-003: Deep Brief — предложения мест, модерация и пользователи

## Note

Пользователь предлагает место через русскоязычный пошаговый диалог; один из трёх численно авторизованных модераторов принимает окончательное решение. Подтверждённое место автоматически дополняет поиск через durable SQLite overlay без записи в базовый JSON. Реестр новых взаимодействующих людей доступен только администраторам. Это intake Brief выбранного Route 3 / SPARC + Hexagonal / Deep, а не разрешение реализации или подтверждение полезности.

## Intake and provenance

Исходный запрос дословно: «Продолжай: добавь кнопку «Предложить место», заявку по полям JSON, модерацию для @anastyyyyad, @mxmknn и @oks_ssn и просмотр пользователей бота только для администраторов.»

Согласовано: SQLite для durable proposals и registry; numeric allowlist; решение любого одного модератора атомарно; approved автоматически входят в поиск; базовый JSON read-only. Три numeric ID уже предоставлены владельцем приватно; их отсутствие в документе не blocker. Конфигурация этих значений только в .env, без значений в исходниках, артефактах, commit или логах; .env не читался и не изменялся. Указанные usernames — только человекочитаемые обозначения, не источник прав.

Baseline: committed f956d55; ветка codex/place-submissions согласно intake. Старый релиз всё ещё ожидает ручную приёмку route/URL: этот Brief её не закрывает. Прочитан pipeline: route=3, depth=deep, phase=brief, dev_unlocked=false. Только новый NOTE разрешён к мутации через role-scoped MCP; source/test/helper scripts, Git, pipeline, Evidence, activation, score/score-all исключены. В физическом запуске creator Telegram APIs и Docker не вызывались, приватные файлы и tokens не открывались; последующие операционные проверки основного оркестратора отдельно атрибутированы в разделе Risks.

Прочитаны active baseline через MCP (статус metadata авторитетнее исторического draft текста внутри body):
- PRD-001 updated_at=2026-10-18T20:51:11.875851+00:00.
- SPEC-001 updated_at=2026-10-18T20:51:12.611918+00:00.
- ADR-001 updated_at=2026-10-18T21:37:59.335862+00:00.
- RFC-001 updated_at=2026-10-18T21:37:59.988494+00:00.

Выборочно прочитаны models.py, catalog.py, config.py и вход/планировщик/shutdown telegram_app.py. Сейчас Coworking имеет 13 полей; catalog._record реализует строгую нормализацию и URL/rating/date правила. Application не хранит FSM/user context, получает message/edited_message с limit=1, использует FIFO и global64/chat8. RequestService использует исходный snapshot. Следовательно durable workflow требует явного изменения прежних ограничений «без БД/admin/durable queue», а не утверждения, что baseline уже поддерживает новый scope. Health выполнен; сообщает прежние at-risk/advisory/duplicate замечания, не служит gate PASS и не требует исправления чужих артефактов в этой задаче.

## Problem, users and outcome

Сейчас пользователь не может передать структурированное предложение внутри бота, модераторы не имеют durable очереди решения, администраторы не видят минимальный реестр взаимодействовавших людей. Требуемый результат — контролируемое пополнение подборки и ограниченная операционная видимость без истории поиска. Исследования спроса, текущие объёмы и экономический эффект не предоставлены; календарный срок и SLA не придуманы.

Участники: заявитель в личном чате; три настроенных модератора, каждый с самостоятельным правом решения; администратор с правом /users и /pending; оператор durable state и восстановления. Предлагается единая настроенная тройка для модерации и административных утилит; разделение ролей, если понадобится, должно быть явно определено PRD.

## Hypotheses

### Hypothesis H1 — do nothing

Сохранить read-only JSON и текущий поиск, предложения принимать вне бота. Минимум новых отказов и хранения, но отсутствуют запрошенные кнопка, модерация и /users. Отклонена по несоответствию поручению; это не доказательство экономической выгоды H3.

### Hypothesis H2 — reduced manual queue

Собирать сокращённую заявку и отправлять в ручную очередь, а каталог обновлять оператором с перезапуском. Меньше интеграционных обязательств и транзакционных состояний, но не обеспечивает согласованное автоматическое включение после approval, полный JSON-контракт и durable восстановление всего workflow. Отклонена для выбранного scope; могла бы быть альтернативой только при отдельном сокращении требований владельцем.

### Hypothesis H3 — selected durable workflow

SQLite хранит минимальный реестр, черновики, заявки, approved overlay и outbox; один модератор совершает атомарное окончательное решение; поиск читает только committed approved + базовый каталог. Соответствует согласованному Route 3. Цена: миграции, backup/rollback, удержание персональных данных, конфликтующие решения и неопределённость отправки уведомлений. Принята как направление Brief, проверяемое будущей приёмкой, без фиктивного PASS.

Дедукция: H1 не даёт результата; H2 теряет обязательные свойства; H3 покрывает их при соблюдении изоляции/атомарности/приватности. Индукция ограничена требованиями и текущим кодом: спрос, фактическая нагрузка и удобство wizard ещё не подтверждены. Поздние PRD/SPEC/ADR/RFC должны сравнить конкретные реализации H3 и закрыть оставленные ниже решения.

## Scope and user journeys

Кнопка «Предложить место» открывает нумерованный русский wizard из 10 пользовательских полей. Шаги показывают номер и понятное название; «Назад», «Пропустить» только для optional, «Отмена», предпросмотр и явная «Отправить». Обязательные значения нельзя пропустить. После ошибки пользователь исправляет поле без потери остальных допустимых значений; при отмене заявка не поступает в pending. Поведение resume/cancel и срок хранения draft закрепит PRD.

Все 13 ключей сохраняются: id, name, address, latitude, longitude, active, yandex_maps_url, short_review, description, rating_text, rating_source, rating_checked_at, updated_at. Система управляет id/active/updated_at, пользователь их не вводит и не переопределяет. Остальные 10 вводятся через wizard: name, address, latitude, longitude, yandex_maps_url, short_review, description, rating_text, rating_source, rating_checked_at. Обязательность, defaults и conditional requirements соответствуют SPEC-001; rating_source допускает default catalog, optional пропуски не обходят условие рейтинга yandex.

Проверка переиспользует существующий общий валидатор: закрытые ключи, типы, числовые диапазоны, длины, даты, Яндекс URL и rating provenance; wizard не вводит второй расходящийся schema. Не менять allowlist URL, не добавлять произвольный URL cap, не извлекать координаты из адреса/URL и не обращаться к Яндексу. Проверка семантического соответствия филиала/адреса/координат/ссылки остаётся модератору. Конкретный публичный интерфейс переиспользования валидатора решит SPEC/RFC.

Геопозиция места в форме и origin поиска — разные состояния и намерения. Wizard не запускает случайный поиск и не записывает search origin в draft; поиск не меняет поля draft. Предпросмотр показывает введённую заявку и правило модерации. Отправка создаёт durable pending, который никогда не searchable. Approved становится видимым автоматически только после committed approval и остаётся видимым после restart. Rejected не входит в поиск.

## Moderation, authorization and notifications

Каждая административная команда и каждый callback заново проверяют stable numeric sender ID по allowlist и private chat. Это касается /users, pagination, /pending, approve/reject и повторных/устаревших действий. Username, текст callback, пересланное сообщение и факт наличия кнопки не дают прав. Для callback без доступного подтверждённого private chat/context привилегированное действие отклоняется; подробный контракт доступности и привязки определит RFC.

Любой один из трёх модераторов принимает approve/reject. Первое committed решение окончательно; конкурентные и повторные clicks не могут создать второй overlay, второй переход решения или повторный бизнес-эффект. Невыигравший видит актуальный итог; сбой уведомления не отменяет committed решение. Bound между submission/decision/overlay/outbox должен быть доказан будущими транзакционными crash/concurrency проверками; конкретный SQL/locking алгоритм здесь не фиксируется.

О каждой новой заявке уведомления предназначены явно всем трём configured numeric private chats. Межчатовый recipient intent хранится/передаётся явно; нельзя переиспользовать applicant reply binding или его message ID как reply в чужом чате. Отправка модераторам не зависит от username lookup. Сериализованный bounded outbox по каждому target не создаёт бесконтрольный fanout и сохраняет изоляцию чатов. Ambiguous send не replay: после timeout/disconnect/неопределённого принятия нельзя автоматически повторять его, в том числе после restart. Это не exactly-once Telegram delivery; возможен пропуск уведомления. /pending обеспечивает авторизованный recovery, поэтому непринятое/неполученное уведомление не делает заявку недоступной. Политики безопасного retry при достоверном отказе, лимиты, backpressure, uncertain state и recovery UX решат ADR/RFC.

## Minimal registry and privacy

Регистрировать только human sender (is_bot=false) из подтверждённого private interaction начиная с включения новой версии. Durable поля: numeric user ID, ограниченное display name, текущий optional username, first interaction и last interaction. ID — ключ, username изменяем и может отсутствовать; first сохраняется, last обновляется, username очищается при исчезновении. Точную семантику допустимых interaction и timestamp определит SPEC. Не реконструировать исторических пользователей из логов/Telegram, не обещать «всех когда-либо использовавших бота».

/users — только admins, private, с bounded pagination и повторной проверкой прав на каждом переходе; строки безопасно экранированы. /myid — утилита личного чата для показа собственного ID пользователю, без просмотра чужих профилей или прав по username; конкретные значения в документах не публикуются.

Не сохранять поисковые координаты, текст поисковых запросов, телефоны, raw updates или полную историю сообщений; не включать их в logs/backups/outbox. Координаты и описания самого предложенного публичного места необходимы для заявки и явно отличаются от origin поиска. Не собирать дополнительные профильные поля. Регистрационные и модерационные данные не становятся общедоступным каталогом пользователей. Existing bounded cancellation, shutdown, безопасные diagnostics и privacy sinks сохраняются и распространяются на новые DB/outbox ошибки; raw exception dump запрещён.

Минимальное пользовательское уведомление до подачи: «Для работы с предложениями бот сохраняет ваш ID, имя, текущий username и даты взаимодействия. Данные заявки увидят модераторы; одобренное место появится в подборке. Поисковые геопозиции и историю сообщений не сохраняем». Точный текст, доступность уведомления при первом interaction и правила удаления/retention уточнит PRD; не обещать ещё не реализованное удаление данных Telegram или backups.

## Architecture direction and durability

SPARC + Hexagonal: domain/use cases отделены от Telegram и SQLite adapters; существующие чистые модели/поиск/routes/renderer сохраняют границы зависимостей. Один polling instance, базовый каталог read-only, отдельный writable state volume для SQLite users/drafts/submissions/approved overlay/outbox. Не заменять JSON на writable файл и не встраивать DB/state в image/repository. Durable payload минимален, raw SDK objects не персистируются.

Добавить callback_query к allowed_updates, сохранив ordered limit=1, FIFO по чату, global64/chat8, bounded cancellation/shutdown и отсутствие межчатовой утечки. Callback acknowledgment и admin outbox включаются в конечные delivery budgets; нельзя обойти scheduler бесконечными tasks или DB blocking. Числа новых bounds, приоритеты/recovery, связь outbound serialization с текущим FIFO, транзакционные границы, fsync/WAL/busy settings и lifecycle SQLite отложены в ADR/RFC, а не произвольно предписаны Brief.

Согласованная резервная копия durable state и проверяемое восстановление обязательны; для rollback нужна совместимая пара приложения/schema и сохранённых данных. Откат приложения не стирает принятые заявки/реестр/решения; не запускать старую версию против несовместимой схемы, не терять state volume и не повторять ambiguous sends. Конкретные миграции, restore drill, RPO/RTO и stop/start rollout планируются позднее. В этой задаче backup, deployment и migrations не выполнялись.

## Delta vs active baseline

| Category | Изменение |
|---|---|
| Added | «Предложить место», 10-полевой numbered wizard; durable drafts/submissions/registry/overlay/outbox; numeric moderation; /users, /pending, /myid; private notice; callback_query; backup/restore requirements |
| Modified | Источник поиска расширяется base + committed approved; прежнее «нет БД/admin/durable queue» меняется только для согласованного workflow; config получает private numeric allowlist и отдельный state; envelope/admission/privacy/delivery границы расширяются на callbacks и явные recipients |
| Removed | Нет удаляемых существующих функций; отменяются прежние исключения БД/admin/durable queue в указанной узкой области через будущие активные документы |
| Unchanged | Все 13 catalogue keys и validator semantics; read-only базовый JSON; текущий поиск/сортировка/карточки/route links; отсутствие внешнего поиска/геокодинга/live ratings; limit1/FIFO/global64/chat8; bounded shutdown/privacy; старый manual route/URL acceptance остаётся pending |

Вне scope: отдельная редактура /about, web admin panel, импорт исторических пользователей, произвольные рассылки, профильная аналитика, хранение поисковой истории, Telegram/Yandex live calls в этой задаче.

## Measurable acceptance (future, none executed)

| ID | Given / When / Then и измеримый oracle |
|---|---|
| B01 | Private пользователь открывает кнопку: доступны все 10 пользовательских полей и 3 system-managed; 0 возможностей подменить system fields; numbered Russian steps/back/optional skip/cancel/preview/submit проходят согласованную матрицу |
| B02 | Для валидных/невалидных URL, rating provenance, dates, types и bounds результат совпадает с общим validator; 0 расхождений; весь baseline schema regression сохранён |
| B03 | При чередовании формы и поиска минимум двух пользователей: 0 смешений draft/search origin/чужих полей; pending/rejected дают 0 поисковых результатов |
| B04 | После submit и restart pending и draft восстанавливаются по согласованной resume policy; после committed approval место searchable без ручного JSON edit и после restart; bytes/hash baseline JSON неизменны |
| B05 | Повторные approve, concurrent approve/approve и approve/reject от разных модераторов с барьером дают ровно 1 final decision и не более 1 overlay/business effect; crash до/после commit не даёт частичного решения |
| B06 | Каждый из трёх настроенных moderators самостоятельно решает заявку; unauthorized sender, username spoof, nonprivate chat, forged/stale callbacks и pagination дают 0 privileged reads/writes; /myid показывает только собственный ID |
| B07 | Submit создаёт ровно 3 явных recipient intents, по одному на configured private target; 0 чужих applicant reply bindings; bounded per-target serialization проверена при задержке/ошибке одного target |
| B08 | Timeout/disconnect/ambiguous send + restart даёт 0 автоматических replay неопределённой отправки; durable /pending остаётся доступным всем авторизованным модераторам |
| B09 | Registry содержит только новых private human senders и только разрешённые поля; first стабилен, last/current username обновляются; bounded /users pagination не раскрывается другим; 0 реконструированных исторических users |
| B10 | Fault/log/DB/backup inspection на синтетике: 0 сохранённых search coords/text/phones/raw updates/tokens; допускаются только заявленные place fields/registry/минимальные delivery metadata; notice виден в согласованных точках |
| B11 | callback_query обработка и acknowledgment сохраняют limit1, FIFO/global64/chat8, finite owned tasks, bounded cancellation/shutdown; будущие числовые bounds закрыты RFC и подтверждены независимыми fault/concurrency tests |
| B12 | Согласованный backup/restore + compatible rollback drill сохраняет принятые заявки/registry/overlay/decision и не replay uncertain sends; old search/routes offline regressions проходят; старые live route/URL checks остаются отдельной незакрытой приёмкой |

Приёмка функциональная и измеримая, но не фиктивные результаты. Полная матрица сценариев/нагрузки и budgets появится в PRD/SPEC/RFC. Independent verifier отличен от code generator; creator не сертифицирует реализацию.

## Risks, assumptions and unresolved implementation decisions

Подтверждено владельцем: numeric IDs уже предоставлены; SQLite, any-one atomic decision, auto inclusion и Route3 Deep не требуют повторного согласования. Значения ID намеренно отсутствуют. Операционная проверка основного оркестратора 2026-10-19 через getChat, без отправки сообщений, первоначально подтвердила доступные private chats @mxmknn и @oks_ssn с HTTP 200 и совпадающими usernames, а для @anastyyyyad вернула HTTP 400. Последующая операционная перепроверка основного оркестратора 2026-10-19T11:21:35.891445+00:00 подтвердила для @anastyyyyad HTTP 200, private_chat=true и username_matches=true. Таким образом, по зафиксированным getChat-проверкам доступны private chats всех трёх модераторов; сообщений в ходе этих проверок не отправляли. Платформа требует начала private conversation пользователем через /start; при deployment оператор должен повторно проверить доступность, поскольку блокировка бота и сетевые условия могут измениться. Доступность getChat не доказывает доставку уведомлений или работу новой функции: будущие live-проверки доставки заявок всем трём остаются pending. Все три numeric ID предоставлены владельцем приватно и намеренно отсутствуют в документе. Creator не вызывал Telegram APIs; обе операционные проверки атрибутированы основному оркестратору. Наличие ID не гарантирует доставку; durable pending и /pending сохраняют доступ к заявке, но не заменяют начало private conversation получателем.

Открыто для PRD: единый или разделённый admin/moderator scope; wizard resume/cancel/edit-before-submit и подтверждение результата заявителю; retention/удаление drafts/rejected/users/backups; anti-abuse/rate limits; operational owner и пользовательский notice. Не вводить эти решения молча как согласованные.

Открыто для SPEC: schema/versioning state; идемпотентность submit/update admission; collision-free ID namespace и merge ordering/ties; validity при изменении base JSON; точные display-name/page/callback/payload bounds; interaction/timestamp semantics, optional/default UX.

Открыто для ADR/RFC: transactional commit/outbox/overlay visibility и restart recovery; DB access без блокировки event loop; crash durability и journal/backup policy; uncertain send lifecycle без replay; per-target serialization с FIFO и fairness; callback context/auth/ack budgets, backpressure и finite shutdown; migration/rollout/rollback compatibility и RPO/RTO. Brief задаёт проверяемые свойства, а не incidental algorithms.

Tradeoffs: SQLite прост для одного процесса, но добавляет disk/locking/corruption/migration риски; любой один модератор ускоряет решение, но даёт ему полную ответственность; at-most-no-replay для uncertain send допускает потерянное уведомление; /pending компенсирует обнаруживаемость, не гарантирует доставку; minimal registry всё равно персональные данные; отсутствие historical reconstruction означает неполный исторический охват. Масштаб/спрос/нагрузка неизвестны.

## Official references

Официальные страницы прочитаны creator через web 2026-10-19, без Bot API вызовов в этом физическом запуске:
- https://core.telegram.org/bots/api#user — источник stable numeric identity, human/bot marker и optional username; проект хранит минимальный набор.
- https://core.telegram.org/bots/api#callbackquery — sender и контекст callback; проект требует повторной авторизации и acknowledgment.
- https://core.telegram.org/bots/api#sendmessage — явный target chat и отдельные reply parameters; проект использует numeric private recipients и не переносит applicant binding.
- https://core.telegram.org/bots#how-are-bots-different-from-users — private conversation должен быть инициирован пользователем; результаты последующих операционных проверок основного оркестратора и границы их доказательности явно приведены в разделе Risks, а доставка заявок остаётся будущей live-проверкой.

Эти ссылки поддерживают только Telegram boundary; выбор SQLite, atomic state и запрет replay — требования проекта, не обещания Telegram exactly-once.

## Related

| Active parent | Relation |
|---|---|
| PRD-001 | NOTE-003 based_on PRD-001 |
| SPEC-001 | NOTE-003 based_on SPEC-001 |
| ADR-001 | NOTE-003 based_on ADR-001 |
| RFC-001 | NOTE-003 based_on RFC-001 |

## Methodology and status

generator_identity: creator/places-brief-20261019-01
label: brief-intake
requested_depth: deep
status: draft

S10: H1/H2/H3 и анализ альтернатив явные; own-ID forgeplan_reason без сохранения отдельного артефакта должен быть реально попытан после полного body save. S11: problem/personas/scope/delta/risks/acceptance явные. S12: требования и измеримые GWT oracles передаются в последующие PRD/SPEC/ADR/RFC. S13: один новый NOTE через creator MCP, только его update/links/validate; independent Evidence и fresh Guardian по applicable coverage остаются будущими gate requirements. Никакое draft planning не открывает следующую стадию.

MCP new/get template прочитан; его ошибочное шаблонное Status Active заменено явным draft. Runtime schema доступных new/update не предлагает отдельного параметра depth/labels/identity; они явно заявлены в canonical body, фактическую индексацию metadata необходимо проверить по final get. Если metadata останется standard, это честно сообщается как tooling limitation и незакрытое соответствие requested Deep, без обхода role scope, config/pipeline edits или дополнительного артефакта.

Структурная validation и creator hypotheses не являются independent Evidence/activation PASS. Итоги фактических own-ID reason/validation и freeze SHA сообщаются отдельно после MCP результатов. Старые документы не изменяются, новый NOTE остаётся draft.

## Maintenance attribution

maintainer_identity: maintainer/places-brief-rollout-20261019-01
maintenance_date: 2026-10-19
finding_reference: EVID-033, finding 1

Исправлен только фактический rollout prerequisite по атрибутированной операционной проверке основного оркестратора; все остальные продуктовые решения, гипотезы, критерии приёмки и семантика body сохранены. Metadata depth=deep/status=draft и связи неизменны. EVID-032 и EVID-033 сохранены как draft исторические проверки прежней ревизии; это исправление не переименовывает их verdict и не заявляет PASS. Для новой ревизии требуются свежие независимые reviews и Guardian gate.

## Maintenance consistency record

maintainer_identity: maintainer/places-brief-consistency-20261019-02
maintenance_date: 2026-10-19
finding_reference: EVID-034, findings 1–2
operator_recheck_at: 2026-10-19T11:21:35.891445+00:00

Согласованы только фактическая хронология getChat-проверок и атрибуция creator/operator в Risks, Intake и Official references. Функциональные решения, H1/H2/H3, критерии приёмки и прочая семантика сохранены; metadata deep/draft и связи неизменны. Предыдущие reviews остаются неизменёнными историческими записями своих ревизий; для текущей ревизии требуется свежая независимая документарная проверка. Доступность чатов не является PASS доставки, реализации или активации.






