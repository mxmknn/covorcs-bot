---
depth: deep
id: PRD-002
kind: prd
last_modified_at: 2026-10-19T11:40:53.624697+00:00
last_modified_by: codex-mcp-client/0.163.0-alpha.10.2
links:
- target: NOTE-003
  relation: based_on
- target: PRD-001
  relation: refines
status: active
title: 'Предложения мест: русский wizard, модерация и приватный реестр пользователей'
---

# PRD-002: Предложения мест, модерация и приватный реестр
## Progress
Draft; generator identity: creator/places-prd-20261019-01; actual forgeplan_creator / Role A.
Requested Route 3 / SPARC + Hexagonal / Deep. MCP metadata defaults standard; separate Role D must set --depth deep before freeze.
Implementation, tests, independent Evidence and activation are pending; dev_unlocked=false remains an operator-provided pipeline fact.
## Executive Summary
### Vision
Пользователь предлагает место внутри бота; один из трёх администраторов решает заявку, approved автоматически пополняет поиск.
### Problem
Сейчас нет структурированной подачи, durable очереди модерации и минимального просмотра новых пользователей.
Заявитель вынужден передавать данные вне формы, а администратор переносить их вручную и самостоятельно помнить итог. После сбоя сообщения недостаточно, чтобы восстановить принятое обязательство. Новая функция должна сохранять заявку и решение независимо от доступности Telegram, показывать только проверенные места и ограничивать доступ к пользовательским данным. Impact: спрос и объёмы неизвестны; экономический эффект и production SLA не заявляются.
### Target Users
| Персона | Потребность |
|---|---|
| Заявитель | Передать место, исправить форму и узнать durable статус |
| Администратор/модератор | Решить заявку, восстановить очередь и просмотреть минимальный реестр |
| Оператор | Сохранить принятые данные при сбое, обновлении и откате |
### Differentiators
Полный существующий JSON-контракт, приватная numeric авторизация, публикация без редактирования базового файла.
### Hypotheses and decision
H1: оставить ручной сбор вне бота — минимум хранения, но отсутствуют запрошенные функции; отклонена.
H2: wizard и ручное обновление JSON — меньше состояний, но нет автоматической durable публикации; отклонена.
H3: durable заявка, any-one решение, approved overlay и минимальный реестр — покрывают запрос; выбрана.
Tradeoffs: H3 добавляет хранение персональных данных и backup; одно решение быстрее quorum, но один администратор отвечает за качество.
H3 проверяется будущими AC, а не выдаётся за подтверждённую полезность; uncertain send допускает пропуск уведомления ради запрета опасного replay.
## Success Criteria
| ID | Критерий | Current | Target / срок | Измерение |
|---|---|---|---|---|
| SC1 | Полная подача | Функции нет | 10 шагов/13 ключей до rollout | AC1–4, synthetic fixtures |
| SC2 | Решение и поиск | Функции нет | 1 итог/1 overlay; 0 pending/rejected в поиске до rollout | AC5–7 crash/concurrency |
| SC3 | Приватность | Новый registry отсутствует | 0 unauthorized reads/writes до rollout | AC8–10, sink audit |
| SC4 | Восстановление | Нового state нет | 3 recipient intents; 0 uncertain autoreplay до rollout | AC11–13 fault injection |
| SC5 | Совместимость | Legacy active | Все применимые legacy AC сохранены до rollout | AC16, independent regression |
Это release acceptance targets; пользовательская конверсия и нагрузочная ёмкость ещё не измерены.
## Product Scope
### MVP (In-Scope)
Кнопка «Предложить место», /suggest, русский wizard, preview/submit, /myid, /pending и /users по 10 строк.
Одна configured тройка numeric admins одновременно модерирует и видит пользователей: @anastyyyyad, @mxmknn, @oks_ssn — только обозначения.
Durable SQLite на отдельном writable state volume; base JSON read-only; один polling instance.
### Out of Scope
Historical users reconstruction, поиск в интернете, геокодинг, scraping, автоматические рейтинги, web panel, delete/export UI, branding, analytics.
Нет контактов/телефонов/расширенных профилей, вложений, массового JSON-upload, редактирования уже поданной заявки или отмены итогового решения.
### Growth Vision
Расширения требуют отдельного решения; MVP не обещает quorum, многопроцессность или exactly-once/lossless ingress.
### Added / Modified / Removed / Unchanged
Added: durable wizard/drafts/submissions, numeric moderation, overlay, outbox, registry и перечисленные команды.
Modified: PRD-001 Product Scope / Out of Scope «Не нужны БД, Redis, отдельный HTTP-сервер, Mini App или LLM» — только запрет БД заменён SQLite для нового workflow.
Modified: PRD-001 NFR-01 «Приложение не сохраняет историю/координаты после обработки» и AX-08 «0 сохранённой приложением истории» получают узкое исключение для полей публично предложенного места и минимального registry/state; поиск не сохраняется.
Modified: PRD-001 «профили ... административная панель» в Out of Scope — разрешён только минимальный registry через /users; полноценные профили и панель остаются вне scope.
Modified: SPEC-001 Relationships «Реляционной БД, tenant/entity foreign keys и внешних lookup нет» остаётся про base catalog validator; новый workflow использует отдельную БД.
Removed: только применимость прежнего запрета durable state/очереди к новому submission/outbox; никаких иных legacy требований не удалено.
Unchanged: PRD-001 FR-01–08, AC-01–18 и AX сохраняются нормативной ссылкой, кроме явно названных локальных исключений и дополнения /start.
Unchanged: SPEC-001 C01–C08, T01–T24, строгий base startup, active filtering, ranking/ties, лимит результатов, карточки, маршруты и privacy origin.
Новые поля и ограничения UI не меняют file catalog acceptance; старый route/URL manual acceptance остаётся открытым.

## User Journeys
| Journey | Действия / результат | Failure outcome | Trace |
|---|---|---|---|
| J1 Заявитель | /start → notice → /suggest → 10 шагов → preview → submit → номер/status | Invalid остаётся на шаге; capacity не принимает; retry показывает существующий итог | FR-001–4, AC1–4/13 |
| J2 Администратор | intent или /pending → preview → approve/reject → committed итог | Unauthorized отказ; проигравший видит итог; send failure не отменяет решение | FR-005–7, AC5–8/11 |
| J3 Администратор | /users → страницы по 10 → актуальные данные | Любая страница заново проверяет права; stale cursor даёт безопасное обновление | FR-008, AC9–10 |
| J4 Оператор | согласованный backup → deployment → restart/rollback | Невалидный state не заменяется пустым; admission закрыт до восстановления | FR-009, AC12–15 |

## Functional Requirements
- [ ] FR-001: Заявитель может открыть/возобновить/перезапустить/отменить форму (J1).
- [ ] FR-002: Заявитель может ввести 10 полей с общей валидацией и preview (J1).
- [ ] FR-003: Заявитель может отправить форму один раз и повторно узнать статус (J1).
- [ ] FR-004: Заявитель может искать без изменения draft и видеть собственный /myid (J1).
- [ ] FR-005: Каждый configured admin может окончательно approve/reject pending (J2).
- [ ] FR-006: Admin может открыть /pending независимо от доставки уведомлений (J2).
- [ ] FR-007: Пользователь может искать committed approved сразу и после restart (J1,J2).
- [ ] FR-008: Admin может читать минимальный registry страницами по 10 (J3).
- [ ] FR-009: Оператор может сохранить/восстановить согласованное durable состояние (J4).

### Form and commands policy
/start сохраняет legacy приветствие и location кнопку, добавляет «Предложить место», краткий notice и при наличии draft/status — действие продолжения.
/suggest и кнопка ведут к одной форме; при draft показать «Продолжить», «Начать заново», «Отмена»; restart требует подтверждения удаления draft.
Draft один на user; TTL 7 суток с последнего изменения; /start и поиск TTL не продлевают. После restart процесса незавершённый draft возобновляется.
«Назад» сохраняет допустимые поля; изменение rating/source заново проверяет зависимости; «Пропустить» только optional; «Отмена» удаляет draft без pending.
Шаги: 1 Название/name; 2 Адрес/address; 3 Широта/latitude; 4 Долгота/longitude; 5 Ссылка Яндекс/yandex_maps_url.
6 Краткая оценка/short_review; 7 Описание/description; 8 Рейтинг/rating_text; 9 Источник/rating_source; 10 Дата проверки/rating_checked_at.
Система задаёт id (неизменяемый, уникальный относительно base+overlay), active=true только для approved поиска, updated_at=UTC date approval; пользователь их не редактирует.
Все 13 ключей Coworking неизменны; optional отсутствуют/None по SPEC-001 serialization; pending/rejected не становятся searchable через active.
Обязательны name/address/latitude/longitude; optional skip даёт None, rating_source skip — catalog; null source не новый допустимый тип.
Общий validator SPEC-001 C01–C08: trim/длины, finite ranges, exact source, Gregorian dates, Yandex URL grammar и conditional rating сохраняются.
Wizard разбирает явные numeric поля, не подставляет bool/string в модель; не выводит координаты из адреса/URL, не fetch URL, не придумывает рейтинг.
При rating_text+yandex URL/date обязательны: preview не отправляется до исправления зависимого поля с понятной ошибкой.
Preview показывает все введённые значения, system правила и «Отправить»/«Изменить»/«Отмена»; submit повторно валидирует полный объект.
Raw text ввода — поле только при активном шаге; команды не значения. Поиск доступен отдельным действием «Поиск» с приостановкой формы.
Любая произвольная location/venue — только search origin, никогда поле места; даже на шагах 3/4 предложить числовой ввод, не копировать location в draft.
Search origin живёт только в пределах запроса; форма не меняет origin, поиск не меняет draft. /myid в private показывает только собственный numeric ID.
Повторный /suggest после submit показывает последний статус и действие новой формы; pending лимит исключает второй submit, но статус доступен.
Заявитель видит номер и pending только после commit; approved/rejected подтверждаются bounded уведомлением и свежим чтением через /suggest.
Недоставка подтверждения означает «ответ не подтверждён», не «заявка потеряна»; повтор submit того же preview возвращает тот же номер/итог.

### Moderation, publication and delivery policy
Все admin команды, callback и page проверяют private context и numeric from_user ID на каждом доступе; username не авторизация.
Callback должен быть привязан к доступному private сообщению данного admin и заявке; отсутствующий/чужой/inline context отклоняется.
Любой один admin решает; первое committed решение окончательно. Repeated/concurrent/crash/replayed действия дают один итог и максимум один overlay.
Approve атомарно фиксирует решение, публикацию и необходимые recipient intents; reject фиксирует итог без overlay. Частичный business outcome недопустим.
Новый поиск после commit видит base+approved; уже начатый поиск может завершиться на своём согласованном snapshot.
При сборке snapshot порядок base сохраняется; overlay добавляется после base в порядке committed approvals. При поиске результаты сортируются по возрастанию расстояния, а при точном равенстве расстояний — по возрастанию id, согласно унаследованному контракту PRD-001/SPEC-001.
Коллизия с base/overlay не заменяет запись молча: admission/approval отказывает безопасно, pending остаётся доступным, оператор исправляет конфликт.
Каждый submit создаёт ровно 3 durable явных recipient intents к configured private chats; applicant reply binding/message ID в них не переносится.
/pending: oldest-first, 10 на страницу, текущий status и решение; прочтение не означает повтор неизвестной отправки.
Outbox хранит минимальную ссылку/цель/статус; содержимое берётся из заявки, без raw update, origin и чужих reply parameters.
Per-target очередь сериализована и ограничена 1024 unsettled intents; applicant имеет максимум 2 unsettled status intents.
До принятия submit резервируется capacity всех 3 intents и pending; при недостатке никакого partial acceptance.
До решения резервируется applicant status intent; при заполнении решение не меняется, admin получает явное «повторите после восстановления доставки».
Attempt не более 10 секунд, суммарный budget отправки одного intent 60 секунд; максимум 2 попытки текущего сообщения только после достоверного Telegram 429 с валидным retry_after и общим ожиданием не более 15 секунд, согласно сохранённой baseline send policy. Timeout/disconnect, 5xx и неоднозначные ответы не являются разрешением повтора.
Timeout/disconnect/неопределённое принятие или crash в sending → uncertain; автоматического replay нет, включая restart.
Uncertain/terminal intents освобождают unsettled capacity; /pending и /suggest дают recovery без повторной отправки uncertain intent.
Итог в БД авторитетен; уведомления не exactly-once. Новая явная status-команда — новое чтение/ответ, не replay старого send.

### Registry, admission and retention policy
Registry только для новых human is_bot=false private messages/валидных private callbacks после rollout, не для edited replay, groups, channels или service updates.
До первой registry записи отправляется notice; до завершения попытки отправки durable registry не создаётся. При неуспехе notice registry откладывается до следующего interaction.
Текст: «Бот сохраняет ваш ID, имя, текущий username и даты взаимодействия. Заявку увидят модераторы; одобренное место появится в поиске. Поисковые геопозиции и историю сообщений не сохраняем».
Notice также в /start, /help и перед preview; новые данные сохраняются для работы, без заявления о полученном consent.
Registry: numeric ID, display name до 128 Unicode code points, текущий optional username до 32, first_seen/last_seen UTC времени принятого interaction.
first_seen неизменен; last_seen монотонен; исчезнувший username очищается. /users сортирует last_seen descending с ID tie, не показывает submissions.
Не хранить search coords/messages/phone/profile/raw updates; место и его public координаты — только в draft/submission/overlay.
Defaults: максимум 1 pending/user, 3 successful submissions/user за rolling 24h, 1000 pending total, 10000 drafts и 10000 registry rows.
При registry capacity новые workflow admission закрыты; поиск и /myid остаются доступны без новой registry записи; safe notice сообщает временную недоступность.
Draft 7d; rejected payload и applicant binding 30d после решения; registry 90d бездействия; approved public record и pending без автоматического TTL.
Applicant binding approved удаляется через 30d; payload approved остаётся как публичный каталог. Registry TTL не каскадирует pending/approved.
Terminal outbox personal metadata удаляется через 7d; компактный неперсональный no-replay/decision tombstone сохраняется пока существует submission/overlay.
Предыдущие preview tokens после очистки не принимаются: неизвестный/expired token требует новой формы, не создаёт заявку replay.
Нет автоматического удаления pending/published ради capacity; disk full/лимит → отказ до acceptance, draft по возможности сохранён; /pending показывает backlog.
Cleanup startup и не реже раза в час, batches максимум 100 записей, проход максимум 2 секунды; expiration проверяется и на чтении, просроченное не возвращается.
Backups access-restricted: файл 0600 и каталог 0700, daily и перед migration, retention 7d; удалённое может оставаться только в backup до истечения этого окна. Политика шифрования диска/внешнего backup определяется оператором окружения; новое шифрование, ключевой сервис или криптографическая зависимость не добавляются в этот scope.
Эти консервативные bounds ограничивают неизвестную нагрузку и privacy exposure; они не cap длины catalog URL/файла. При exhaustion оператор восстанавливает место/доставку, затем admission возобновляется.

## Non-Functional Requirements
| ID | Requirement / metric | Condition / measurement |
|---|---|---|
| NF1 | 0 unauthorized admin reads/transitions; 0 sensitive diagnostics | Все команды/страницы, negative auth и sink audit |
| NF2 | Ordered polling limit=1, FIFO/chat, global64/chat8 сохранены | Callback ingress и outbox включены; instrumentation fault checks |
| NF3 | 0 duplicate publication/decision, committed durable после restart | Kill до/после каждого commit, concurrent/replay checks |
| NF4 | 0 uncertain autoreplay; 3 явных targets на submit | Fake sender timeout/crash/restart oracle |
| NF5 | Existing finite cancellation/send/shutdown budgets не увеличены | Baseline lifecycle regression; новые sends в тех же общих пределах |
| NF6 | Cleanup ≤100/batch и ≤2s/pass; pages ≤10 | Synthetic expiry/capacity checks; без бесконечных background tasks |
| NF7 | Backup RPO ≤24h; planned restore drill RTO ≤60min | До rollout измерить на согласованном snapshot; unbacked host loss — residual risk |
БД не блокирует event loop без конечного budget; exact schema/locks/fsync/migrations и Telegram chunking определит SPEC/ADR/RFC.

## Acceptance Criteria
Все проверки ниже будущие, не выполненные; слова Given/When/Then задают измеримый oracle.
| AC / trace | Given | When | Then |
|---|---|---|---|
| AC1 FR-001 | Private human, нет draft | /start, /suggest | Notice до registry; обе main кнопки; шаг 1/10 |
| AC2 FR-001–2 | Заполнены шаги 1–4 | Back, optional skip, cancel, resume/restart | Допустимые поля сохранены; required skip запрещён; cancel без pending; restart только с подтверждением |
| AC3 FR-002 | Все SPEC boundaries и rating variants | Preview/submit | Одинаковое acceptance C01–C08; 13 прежних ключей; invalid не принимается |
| AC4 FR-003 | Один valid preview | Двойной submit, crash/replay | Один номер/pending, 3 intents; повтор видит тот же итог |
| AC5 FR-005 | Pending, два authorized admin | Одновременные approve/reject | Один committed итог; второй видит его; overlay 0 при reject или 1 при approve |
| AC6 FR-007 | Committed approved и pending/rejected | Новый поиск, restart, поиск | Approved присутствует оба раза; pending/rejected отсутствуют |
| AC7 FR-005/7 | Fault до/после decision commit | Kill/restart/replay | Ни одного частичного решения/overlay; нет duplicate |
| AC8 FR-005–6 | Group/forged username/чужой или inaccessible callback | Любая admin команда/page/action | 0 чтений registry/pending и 0 переходов; safe отказ |
| AC9 FR-008 | 23 registry users | /users и все pages | 10/10/3, повтор auth, escaped name; никаких search/submission данных |
| AC10 FR-008 | Новый private human, bot/group, смена username | Interactions/TTL | Только human private зарегистрирован; first stable/last monotonic; username очищен; TTL скрывает expired |
| AC11 FR-006 | Один модератор недоступен, один timeout | Delivery и restart | Три отдельных target intents; чужих reply IDs нет; uncertain не replay; /pending доступен |
| AC12 FR-009 | State snapshot и compatible backup | Restore/restart | Сохранены pending/решения/overlay/uncertain; потеря не больше backup RPO, measured RTO |
| AC13 FR-003 | Pending/ratelimit/outbox/disk capacity exhausted | Submit/retry | Явный отказ до acceptance; ни partial intents, ни тихого drop; восстановление допускает retry |
| AC14 FR-004 | Draft и произвольная location/venue | Поиск и возврат | Origin не стал place field, draft не изменился, origin не durable; /myid только свой |
| AC15 FR-009 | Expired draft/rejected/registry, живые pending/approved | Cleanup и stale callback | Bounds соблюдены; expired не читается, pending/approved сохранены, stale token не submit |
| AC16 FR-004/7 | Legacy synthetic suite и real owner acceptance pending | Regression | PRD-001 применимые AC/AX и SPEC-001 T соблюдены; ручные route/URL не объявлены PASS |
| AC17 FR-003 | Commit есть, applicant notification blocked/timeout | /suggest после restart | Durable номер/status показан; решение сохранено; нет бесконечного retry |
| AC18 FR-009 | Несовместимая schema/битый state | Startup/rollback | Новый workflow закрыт, state не обнулён, safe diagnostic; восстановление совместимой пары |

## Dependencies
| Dependency | Status | Owner / boundary |
|---|---|---|
| Active NOTE-003 | Прочитан; active/deep, updated_at 2026-10-19T11:35:41.915321+00:00 | Parent canonical body SHA44705d2681009fce78e87c862ef5ef1536b4fa5783af73454e357ea48cc555b3 |
| Baseline PRD-001 / SPEC-001 | Active; прочитаны relevant clauses | Нормативное сохранение legacy |
| Numeric config всех 3 | Приватно предоставлена; не missing | Оператор; значения здесь не читаются/публикуются |
| SPEC / ADR / RFC | Будущие | Алгоритмы, schema/versioning, transactions, callback/chunk bounds, validator interface, compatibility |
Operator-provided operational fact: root подтвердил все три private numeric chats и usernames; delivery не проверена. Creator Telegram не вызывал.

## Risks & Mitigations
| Risk | Probability / impact | Mitigation / owner |
|---|---|---|
| Неизвестные спрос/нагрузка | Unknown / backlog | Явные admission bounds, /pending; product owner |
| Ошибочное approval | Possible / качество каталога | Admin проверяет адрес/координаты/URL, без ложной semantic certification |
| Disk/corruption/host loss | Possible / data loss | Consistent backup/drill; оператор; RPO не zero-loss |
| Privacy / backup lag | Possible / personal exposure | Минимизация и TTL, restricted backups; оператор |
| Telegram uncertainty/block | Possible / missed notice | No autoreplay, durable status и /pending; runtime owner |
| Очень длинный valid URL | Possible / UI failure | SPEC/RFC bounded chunk/input assembly без schema cap; transport предел честно объясняется |
Unresolved material assumptions: реальная нагрузка, качество пользовательских мест, доступный storage/backup budget не подтверждены.
Delivery всем трём и реальные route/URL требуют будущей ручной проверки; наличие numeric IDs не unresolved assumption.

## Timeline
| Milestone | Target | Exit |
|---|---|---|
| PRD freeze | После отдельного Role D depth=deep | Независимые reviews/ADI и Guardian по frozen revision |
| SPEC / ADR / RFC | После active PRD; дата не обещана | Algorithms/schema/durability/chunking/readiness закрыты |
| Build / Prove | Только active RFC и unlock-build | Независимые AC1–18 и legacy regression |
| Rollout | После independent PASS и backup drill | Private staged проверки всех 3 recipients и status recovery |
| Rollback | По отказу smoke/миграции | Stop admission, consistent snapshot; совместимые app/schema, не старое app против новой БД |
## Rollback Plan
Rollback сохраняет state volume; pending не удаляются. Старый read-only режим допустим только с явной паузой workflow и сохранённым overlay/search совместимым путём.
Если rollback теряет отображение approved, сервис не объявляется восстановленным; оператор восстанавливает совместимую пару. Backup restore честно сообщает возможную RPO потерю.

## Stakeholders
Product owner — пользователь; три configured admin — moderation/registry; оператор deployment/backup — владелец текущего локального развёртывания и репозитория; при передаче эксплуатации он назначает нового оператора.
Creator создаёт требования; независимые verifier/ADI/Guardian дают будущие проверки. Creator не сертифицирует свою работу.

## Affected Files
Будущие кандидаты: coworking_nearby/telegram_app.py, catalog.py shared validation boundary, models.py, config.py и новые state/domain adapters; tests/docs позже.
Сейчас source/tests/helpers/private config не изменяются. SPARC + Hexagonal сохраняет pure search/routes/render границы; SQL и алгоритмы принадлежат RFC.

## Related Artifacts
Фактические MCP graph links: PRD-002 based_on NOTE-003 (active); PRD-002 refines PRD-001 (active). Autoactivation=false.
SPEC-001 active — нормативная ссылка C01–C08, не новый изменённый artifact; baseline f956d55 / codex/place-submissions — operator-provided context.
S10: H1–H3 и own-ID reason attempt; S11: journeys/FR/risks/AC; S12: explicit behavior contracts; S13: scoped new/update/link/validate.
Все S10–S13 применимы; 100% coverage, active independent Evidence и fresh Guardian требуются отдельно до activation. Этот draft следующую стадию не открывает.

Own-ID forgeplan_reason(save=false) фактически отказал: «MCP tool call requires approval, but approval policy is never»; reasoning result отсутствует, обход не предпринимался.

## Maintenance consistency record

maintainer_identity: maintainer/places-prd-consistency-20261019-01
maintenance_date: 2026-10-19

По точному предписанию основного оркестратора согласованы только baseline send policy, минимальные права доступа backup и ответственность текущего оператора. Исходный creator и все остальные решения, требования, критерии приёмки, metadata deep/draft и связи сохранены. Эти уточнения не являются доказательством реализации или активации.





