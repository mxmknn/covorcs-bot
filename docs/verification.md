# Наблюдения Build — coder/coworking-20261019-01

Дата клиента: 2026-10-19. Это отчёт генератора кода, не независимая сертификация, Guardian PASS, активированное Proof/Evidence или разрешение Ship. Изменения ForgePlan artifacts, pipeline, ролей, Git index и commits не выполнялись. Единственный физический coder в этой волне. NOTE-002 (Working Moscow и `/about`) остаётся отдельным draft и не реализован.

## Авторизация и границы

Прочитаны AGENTS.md и физический `.codex/agents/forgeplan-coder.toml`. `forgeplan health` завершился exit 0: healthy, advisory phase mismatches. `python3 .codex/forgeplan-pipeline.py status` завершился exit 0: phase=build, dev_unlocked=true, rfc_id=RFC-001, prd_id=PRD-001. Scoped read-only MCP get получил RFC-001, PRD-001, SPEC-001, ADR-001, EVID-021; metadata active. RFC based_on PRD-001/SPEC-001; historical draft prose не меняет metadata. RFC updated_at=2026-10-18T21:37:59.988494+00:00; SHA256 точного MCP body, независимо вычисленный Python hashlib: `e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177`.

Разрешённые изменения этой волны: `coworking_nearby/telegram_app.py`, `coworking_nearby/__main__.py`, `tests/test_telegram_app.py`, `tests/test_privacy.py`; новые `README.md`, `Dockerfile`, `compose.yaml`, `docs/verification.md`, `tests/test_packaging.py`. `tests/conftest.py` не изменён, offline socket guard сохранён. Зависимости/locks/domain/render/config/catalog/models, данные и `.env.example` не менялись. Настоящий `.env` не читался, не хешировался, не копировался, не передавался в daemon и не использовался в контейнерах. Все контейнерные credentials — пустые или явные synthetic fake.

Предыдущий baseline 668 passed/8.36s был передан parent; в этой волне исходный baseline до правок не запускался повторно и supplied frozen hashes до правок независимо не измерялись. Текущая полная suite включает все прежние тесты, без удаления/skip. `git rev-parse --verify HEAD` фактически exit 128, `fatal: Needed a single revision`: unborn, нет HEAD. CI в этой волне не запускался; CI результатов не заявлено.

## Реальные RED/GREEN и отклонения

Сначала добавлены поведенческие проверки, затем выполнено:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_telegram_app.py::test_raw_location_array_metadata_stops tests/test_telegram_app.py::test_queue_wait_measured_separately_from_service_deadline tests/test_privacy.py::test_safe_verbosity_threshold_and_nested_restoration tests/test_privacy.py::test_run_defers_caller_cancellation_until_acquired_session_closed
```

Наблюдалось **11 failed, 3 passed in 2.37s**: queue timing отсутствовал; set_level отсутствовал во всех восьми случаях; run не пробрасывал отмену или cleanup fail-stop после barrier cleanup. Три raw array metadata случая уже были GREEN благодаря текущему SDK; RED для них не заявлен. Историческое удаление исправного поведения ради RED не выполнялось. Добавлен явный DeliveryStop до SDK для nonobject metadata, чтобы не полагаться на SDK coercion; ограничения invalid-coordinate dict и valid venue/backcompat сохраняются.

Изменения: frozen `_Admission` содержит только envelope и monotonic admission timestamp. Scheduler записывает admission-to-worker-start wait отдельно от RequestService service90, без await в commit/ownership/cursor/rollback. DEBUG queue event имеет насыщаемое wait_ms 0…86400000; нет истории завершённых запросов. Виртуальная задержка очереди 120 секунд не расходует 90-секундный service budget; отдельные прежние service deadline/fault тесты сохранены. Существующий timeout attempt 10 секунд проверяется отдельно.

`run()` запоминает первую и последующие caller cancellation, ждёт единственный cleanup coordinator и затем пробрасывает CancelledError. Ошибка close/cleanup имеет приоритет FailStop. CLI переводит штатную отмену в exit 0 и fail-stop в exit 1; asyncio.run с неограниченным cancel-all не добавлен. Barrier-тест отменяет после приобретения ресурсов, повторяет отмену во время close и доказывает, что закрытие завершается до результата.

LOG_LEVEL применяется только к fixed safe event emitter. DEBUG/NOTSET допускают queue; INFO — start; WARNING/WARN — warning/stop; ERROR — fail; CRITICAL/FATAL отфильтровывают текущие менее серьёзные события. Nested ProcessSinks восстанавливает предыдущий порог и sink. INFO/DEBUG adversarial tests фактически устанавливают safe threshold; raw library/root/warnings/loop по-прежнему блокируются до форматирования. hostile str/repr и вложенные исключения не форматируются.

После минимальных исправлений полный host run: **682 passed in 8.31s**. Это включало все прежние 668 и 14 новых случаев.

Release RED: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_packaging.py` сначала дал 2 failed/3 passed; первая версия теста ошибочно предполагала доступный YAML parser. После удаления этого предположения повторный RED дал 2 failed/3 passed in 2.07s именно по отсутствующим Dockerfile/compose. Compose записан в JSON-подмножестве YAML и проверяется stdlib. После создания release files: **5 passed in 2.17s**. Проверки нормативные: exact digest, require-hashes/public index, закрытый COPY список, unprivileged user, один CMD, отсутствие devdeps/ports, image-only Compose, read-only directory bind, пустой рабочий и отдельный synthetic каталог; executable blank-token failure и inert/standalone CLI с запретом SDK/network. Никакой Docker skip/условного PASS в pytest нет.

В этой волне не восстанавливались индивидуальные RED для исторических acceptance cases прежних волн. Их TDD chronology независимо не подтверждена. Документирование и уточнения существующей защиты metadata не имеют искусственно изготовленного RED.

## Историческая проверка перед fresh narrow repair

| Среда/команда | Наблюдение |
|---|---|
| Host `.venv/bin/python -c 'import sys,platform;print(sys.version);print(platform.platform());print(platform.machine())'` | Python 3.12.15, Clang 23.1.3, macOS-27.0.1-arm64-arm-64bit, arm64 |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q` | **688 passed in 10.55s**, exit 0; предыдущий финальный run 688/10.20s |
| Docker client/server | client 29.4.3 darwin/arm64; server 29.4.3 linux/arm64, Docker Desktop 4.73.0 |
| Runtime interpreter | Python 3.12.15, GCC 12.2.0, aarch64; UID 10001 |
| Linux test image install | public PyPI, полный requirements-dev.lock с --require-hashes, exit 0 |
| `docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test` | **688 passed, 1 warning in 12.77s**, exit 0; без skip |
| Runtime catalog CLI, real [] | exit 0, без вывода |
| Runtime catalog CLI, synthetic read-only mount | exit 0, без вывода |
| Runtime blank BOT_TOKEN | exit 1, ровно одна JSON fail/startup строка, stdout пуст |
| Runtime inspect script | expected /app whitelist, no .env/tests/.forgeplan/.venv, no pytest/setuptools distributions, catalog mode без write bits |
| Compose copied file + empty temporary env, config --quiet | exit 0, без вывода |
| Fake-token offline startup/SIGTERM | safe events start/stop, exit 0, stop+inspect 0.599s; network none, read-only filesystem |

Первый Linux run: **685 passed, 2 failed, 1 warning in 13.54s**. Причины: в staging не скопировали blank `.env.example`; исходный ManualClock унаследовал Linux monotonic resolution 0.001 секунды, и asyncio мог запускать timeout на 1ms раньше. Targeted rerun воспроизвёл timeout failure. Фактический `time.get_clock_info("monotonic")` в контейнере сообщил resolution=0.001. ManualClock теперь задаёт 1e-9 только для виртуального времени и восстанавливает исходное значение; sleep не продвигает часы. Существующее строгое утверждение pending на 9.999 и завершение на 10 секунд сохранено. Staging исправлен, все tests restaged; последний Linux run выше GREEN. В неудачном run после assertion был unclosed-client diagnostic; в финальном run его нет. Единственное финальное предупреждение — pytest unknown config option cache_dir, ожидаемо при `-p no:cacheprovider` на read-only suite; cache не записывается.

## Контейнерные команды и контекст предыдущей волны

Все docker calls этой волны использовали локальный daemon и изолированный **Docker** client config в ignored `.venv/verification/docker-config` (не Codex config). Не читался existing Docker secret config. Общий префикс после инициализации пустого config:

```sh
export PATH=/Applications/Docker.app/Contents/Resources/bin:$PATH
export DOCKER_CONFIG="$PWD/.venv/verification/docker-config"
export DOCKER_HOST=unix:///Users/mxmknn/.docker/run/docker.sock
```

При первом build default buildx не смог записать activity вне writable roots. Legacy tar затем встретил macOS xattr; Python PAX archive не распознался legacy builder. Эти попытки не были успешными builds. Успешная сборка использовала USTAR и явный whitelist:

```sh
python3 -c 'import sys,tarfile; from pathlib import Path; t=tarfile.open(fileobj=sys.stdout.buffer,mode="w|",format=tarfile.USTAR_FORMAT); paths=[Path("Dockerfile"),Path("requirements.lock"),*sorted(Path("coworking_nearby").glob("*.py")),Path("data/coworkings.json")]; [t.add(p,arcname=str(p),recursive=False) for p in paths]; t.close()' | docker build -t coworking-nearby:local -
```

Результат: runtime image `f883f293ecc9`, successful build/tag; контекст 143.4kB, не весь repo. Base exact `python:3.12.15-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258`. Runtime pip install фактически download/install из https://pypi.org/simple с --require-hashes, без private mirror. Есть ожидаемый pip root warning на build stage. Apt не используется.

`/app` фактически содержит девять `coworking_nearby/*.py`, `data/coworkings.json`, `requirements.lock`. Дополнительные distributions базового образа включают pip 25.0.1; dev dependencies в runtime не установлены. Установленный runtime: aiofiles25.1.0, aiogram3.31.0, aiohappyeyeballs2.7.1, aiohttp3.14.5, aiosignal1.4.0, annotated-types0.8.0, attrs26.1.0, certifi2026.10.18, frozenlist1.8.0, idna3.20, magic-filter1.0.12, multidict7.1.0, propcache0.5.4, pydantic2.13.5, pydantic-core2.46.5, typing-extensions4.16.0, typing-inspection0.4.4, yarl1.25.1. Linux dev image дополнительно фактически установил iniconfig2.3.1, packaging26.3, pluggy1.7.0, pygments2.21.0, pytest9.1.1, setuptools84.0.0; Windows-only colorama marker не применим.

Для dev test image отдельно staged только все package/test `.py`, real catalog, synthetic example, pyproject.toml, два lock, production Dockerfile, compose.yaml, blank `.env.example` в `.venv/verification/linux`. Временный Dockerfile.test там же: exact pinned base; WORKDIR /suite; COPY requirements-dev.lock; pip public --require-hashes; COPY только staging; USER10001; CMD python -m pytest -q -p no:cacheprovider --basetemp=/tmp/pytest. Никакого whole-repo mount/context. Финальный dev image `a139428248df`.

Фактический dev build передавал USTAR staged files:

```sh
python3 -c 'import sys,tarfile; from pathlib import Path; root=Path(".venv/verification/linux"); t=tarfile.open(fileobj=sys.stdout.buffer,mode="w|",format=tarfile.USTAR_FORMAT); [t.add(p,arcname=str(p.relative_to(root)),recursive=False) for p in sorted(root.rglob("*")) if p.is_file()]; t.close()' | docker build -f Dockerfile.test -t coworking-nearby:test -
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test
docker run --rm --network none coworking-nearby:local python -m coworking_nearby.catalog
docker run --rm --network none -e BOT_TOKEN= coworking-nearby:local
docker run --rm --network none --mount type=bind,src=$PWD/examples,dst=/synthetic,readonly coworking-nearby:local python -m coworking_nearby.catalog /synthetic/coworkings.synthetic.json
docker compose -f .venv/verification/compose.yaml --env-file /dev/null config --quiet
```

Последняя команда использовала **копию** compose и отдельный пустой `.venv/verification/.env`; настоящий local .env не использовался. Для Compose plugin discovery временный Docker config содержал cliPluginsExtraDirs=/Applications/Docker.app/Contents/Resources/cli-plugins. Smoke orchestration через Python subprocess запустил detached runtime `--network none --read-only --tmpfs /tmp:rw,nosuid,nodev -e BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk`, дождался safe start, вызвал `docker stop --time 20`, inspect ExitCode, logs, затем удалил только собственный контейнер. Нет Telegram calls, Yandex calls, registry push или paid publish.

## Что остаётся вне этих результатов

Owner должен предоставить реальные записи одного филиала с городом+домом, координатами, согласованной ссылкой, источником/датой рейтинга; validator не удостоверяет факты и не геокодирует. Рабочий [] и отдельная synthetic data сохранены. Настоящий токен остаётся локальным. BotFather guidance сверено с первичным https://core.telegram.org/bots/tutorial#obtain-your-bot-token; доступность username не проверялась.

Ручная проверка **двух origins**, для одного результата **каждого все три режима**, start/end/mode в браузере — **UNPERFORMED**. Live Telegram startup/delivery и реальное принятие произвольных organisation URLs — **UNPERFORMED**. Mocked platform rejection cases показывают консервативное поведение при известных отказах, не live proof. Неограниченный SPEC-valid organisation URL не имеет универсальной доказанной доставки; полное принятие AC-15/AX-05/NFR-06 не заявлено, cap/truncate/omit не добавлены. Нагрузка, спрос, SLA, произвольные некoopерирующие зависимости и физическое обнуление RAM не измерены. Истории Telegram/браузера не удаляются. Следующий шаг parent — независимый rerun/audit и требуемые отдельные gate решения.


## Fresh narrow repair: strict lower-bound waits, final frozen source

Sole implementer: coder/coworking-20261019-01, after root independent negative verification. Only `coworking_nearby/telegram_app.py`, `tests/test_telegram_app.py`, and this report changed in this repair. README/Dockerfile/packaging tests and all other product files remain unchanged. No artifact/pipeline/config/index/commit mutations or independent certification. No live calls, real .env access, Compose startup, or registry push. Prior 688 results and prior image IDs above are historical, not proof for this final source.

Read AGENTS.md, coder role, pipeline status and forgeplan health (exit0, healthy with advisory phase mismatches). Scoped canonical get independently confirmed RFC-001 active, updated2026-10-18T21:37:59.988494+00:00, exact body SHA256 e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177 (CLI JSON body hashed with Python hashlib); body based_on active PRD-001 and SPEC-001. ADR-001/EVID-021 active. Pipeline phase=build/dev_unlocked=true/rfc_id=RFC-001. Read TC-3 timing/lifecycle and TC-4 release contracts. Initial four supplied frozen hashes independently matched. `forgeplan show` was attempted and rejected as unsupported; read-only get was used instead, no score or activation.

Actual RED command:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_telegram_app.py::test_coarse_clock_strict_lower_bound_waits
```
Observed **2 failed in 2.25s** against original production source. Forced loop._clock_resolution=.001 with existing ManualClock and no automatic advancement. START sent at1.0995, below1.1; positive flood2 wait ended at3.0995 rather than3.1 and began next PAUSE early. Regression records each sleep start/duration/end and actual send times. Production `_wait_full` now captures one loop.time end and awaits remaining repeatedly until nonpositive, for PAUSE and flood wait. Existing service90 deadline, full10 attempt availability checks, retry budget15, zero429, one extra retry, ambiguity/redirect/raw429 guards, cancellation/queue/shutdown code remain intact. Attempt timeout remains an upper bound.

Intermediate first implementation run: one new assertion failed because asyncio repeatedly dispatches the same remaining sleep while manual time is stationary; test now requires every repeated sleep to retain the exact end. An intermediate targeted run was interrupted after21.47s because adding .0005 landed below1.1 in binary floating point; advance now targets `1.1 - clock.now`, with task.done assertion before await. A subsequent full run reported689 passed/1 failed in11.01s: existing retry-budget wait5 test's1.099+.001 advancement similarly landed below the true end. It now advances to `(attempts[1][0] + wait + PAUSE) - clock.now`, preserving pending-before/end-send assertions. No production epsilon, shortened wait, assertion deletion or manufactured RED. Final targeted result **2 passed in2.32s** (before the existing test advancement correction); full final suites cover both cases again.

Final actual checks (all exit0 unless noted):

| Command / observation | Final result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q` with unchanged autouse socket guard | **690 passed in10.95s**, no skips |
| Host identity | Python3.12.15/Clang23.1.3 macOS27.0.1 arm64 |
| Safe USTAR runtime build command above, exact whitelist only | runtime image **sha256:93a6a3263aa5f568ced199483ad74f1f6a9e74ddc7634e258a675e67dc7ee87c** |
| Safe staged USTAR dev build above, `-f Dockerfile.test` | test image **sha256:8a76c52f2adb01bd9cbf26d6c9b3e73f55714406ba6b6bb934aef8a65e204479** |
| `docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test` | **690 passed,1 warning in12.94s**, no skips |
| Runtime Python/arch/UID | Python3.12.15 GCC12.2.0 / aarch64 /10001 |
| Runtime real[] validator / read-only synthetic mount validator | each exit0, empty stdout/stderr |
| Runtime explicit `-e BOT_TOKEN=` | exit1, stdout empty; exactly one safe JSON event=fail/stage=startup |
| Offline fake-token startup, docker stop --time20, inspect/logs | safe start/startup then stop/ingress only; exit0; stop0.529861458s |

Final builds used the existing isolated Docker config and explicit local socket/pinned base as above; buildx now worked without changing global config. Runtime dependencies installed from public PyPI with --require-hashes; dev install from the same exact dev lock (cached in final rebuild). No lock/base changes. Staged final package/tests, blank .env.example only, README, Dockerfile, compose, pyproject, both locks, real[] and separate synthetic example; no repository context/mount. The final Linux image was rebuilt after all source/test changes. Expected warning is cache_dir unknown with disabled cacheprovider; no manifest change. No Compose change/revalidation needed.

Final smoke commands use `docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev` followed by runtime image and `python -m coworking_nearby.catalog`, or `--mount type=bind,src=$PWD/examples,dst=/synthetic,readonly` and catalog `/synthetic/coworkings.synthetic.json`; blank-token invocation adds `-e BOT_TOKEN=` before image. Detached smoke uses the same restrictions and synthetic `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk`, waits for safe start, `docker stop --time 20`, `docker inspect --format '{{.State.ExitCode}}'`, `docker logs`, then removes only that container. Python subprocess captured exit codes/output; stop timing used time.monotonic. No real credentials/env file passed.

Runtime whitelist inspection via container Python Path('/app').rglob found exactly nine package .py, requirements.lock and data/coworkings.json. Runtime telegram_app SHA **805214e5cd585c8ebe0f6c633b421417f7540f79e766e953e4d38d6611ae1da8** equals final host source. Final test SHA **e718356cf86153755e001711ec20625edd1864b1b05b1faeb2346b8e4d318d7d**. Unchanged main SHA9500a1e8dcdcdbea2d61076e46edab17dd7e2dbc93b85495be652c7ac920cbc3; privacy test SHAb5474f0a5a20a8e689e7ee7d2ae76e0b28c741989302a7615d59ec7332893557. Final host selected hashes measured by shasum -a256; runtime selected hashes by hashlib. Repository remains unborn: git rev-parse --verify HEAD exit128. No CI result. All live/manual/platform limitations above remain; these are implementer observations for parent independent inspection/rerun/audit, not Guardian PASS or Ship permission.


## EVID-024 narrow repair v2 — caller cancellation at owned completion

2026-10-19; sole implementer coder/coworking-20261019-01. This section supersedes the earlier “final” 690-test/image observations for changed source. Those observations and EVID-022/023/024/025 remain historical. No independent PASS, Guardian decision, activation or Ship authorization is claimed.

Before writes: read AGENTS.md, `.codex/agents/forgeplan-coder.toml`, full canonical EVID-024 and old audit-freeze.json. Direct execution of pipeline script returned permission denied/126; `python3 .codex/forgeplan-pipeline.py status` returned0, phase=build/dev_unlocked=true/rfc_id=RFC-001/prd_id=PRD-001. `forgeplan health` returned0 with RFC at-risk/advisory phase mismatches; no suggested score was run. Scoped canonical get confirmed active RFC/PRD/SPEC/ADR/EVID-021. RFC timestamp and exact body SHA remain 2026-10-18T21:37:59.988494+00:00 / e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177; its based_on includes active PRD-001/SPEC-001. Four initial supplied source/test hashes independently matched. Old freeze raw SHA remains33c5a02a0e9e778dc1327a65b376726fb975d034dfd8321f46c8cbf25f8f2127; declared files canonical aggregate remains87421c1f474117e6808bfc4584f9752be636edbad51a86ff26036a6197a1b106. Old freeze/proof/artifacts were not rewritten. Parent owns creation of a fresh v2 freeze and independent delta audits.

Changed files only: coworking_nearby/telegram_app.py, coworking_nearby/__main__.py, tests/test_telegram_app.py, tests/test_privacy.py, docs/verification.md. README needs no result correction and is unchanged. No changes to pipeline/config/index/commits, domain, locks, data, conftest or artifacts. NOTE-002 stays separate draft. No real .env read/hash/copy/mount, live service calls, compose up or push.

Actual RED against unchanged production source:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_telegram_app.py::test_owned_completion_caller_cancellation_boundary tests/test_privacy.py::test_owned_completion_caller_cancellation_boundary
```
**6 failed,10 passed in2.53s**, exit1. Both paths failed successful completion plus caller cancellation, and both replaced owned RuntimeError/FailStop with a new FailStop at the same boundary. Already-done and genuine-owned-cancel controls were already green; no RED is invented for these controls. Each path has success/cancel/error/failstop x completion/already_done, 16 new cases total. Completion callbacks plus Event barriers inject repeated caller cancellation without elapsed-time sleeps; sleep(0) only yields ready callbacks. Real Application success runs its owned cleanup/session-close and asserts same coordinator, pending0/workers0. All cases assert no remaining tasks; failed tasks preserve exception identity. Already-done cases cancel caller immediately before awaiting completed owned work.

Small production distinction in both catch blocks: cancelled owned task becomes FailStop; completed noncancelled task.result() retrieves/rethrows its original failure, or confirms success and breaks to deferred caller CancelledError. No retry/new cleanup, deadline reset, unbounded join or runner changes. Existing fixed 2/10/2/2 cooperative stages and full monotonic lower-bound waits remain intact. Targeted GREEN: **16 passed in2.01s**, exit0, same command. Prior AC-by-AC historical RED limits remain as documented above.

Actual verification after final source/test writes:

| Command/observation | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q` | **706 passed in10.23s**, exit0, no skips; unchanged socket guard |
| Host | Python3.12.15 Clang23.1.3, macOS27.0.1 arm64 |
| runtime USTAR build | **sha256:b909f443edde64355c0e76c0aafa65251a4ac4a90001207b9a721b6b911e200a**, exit0 |
| dev USTAR build | **sha256:bdb4dbad98d580edb3e03a5327e2e0c6b6c97447a9e8fc1be746a31611665e78**, exit0 |
| `docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test-v2` | **706 passed,1 warning in12.84s**, exit0, no skips |
| Linux | Python3.12.15 GCC12.2.0 aarch64; pytest9.1.1; exact unchanged runtime/dev dependencies listed above |
| real[] validator / readonly synthetic validator | each exit0, empty stdout/stderr |
| explicit blank BOT_TOKEN | exit1, empty stdout, exactly one safe fail/startup JSON |
| fake-token start/SIGTERM | exit0, stop0.547492209s; only safe start/startup and stop/ingress events; owned container removed |

Both builds used PATH=/Applications/Docker.app/Contents/Resources/bin:$PATH, DOCKER_CONFIG=$PWD/.venv/verification/docker-config, DOCKER_HOST=unix:///Users/mxmknn/.docker/run/docker.sock; no global config edit. Python tarfile USTAR_FORMAT archives in ignored `.venv/verification/v2-linux` were passed as stdin to `docker build -f Dockerfile -t coworking-nearby:v2 -` and `docker build -f Dockerfile.test -t coworking-nearby:test-v2 -`. Runtime archive contains ONLY Dockerfile, requirements.lock, nine package .py, data/coworkings.json. Dev archive contains ONLY staged package/test .py, blank .env.example, README, pyproject, both locks, production Dockerfile, compose, real[] and synthetic example, Dockerfile.test. Dockerfile.test uses same exact pinned3.12.15 base, public PyPI --require-hashes full requirements-dev.lock, COPY safe staging, USER10001, CMD python -m pytest -q -p no:cacheprovider --basetemp=/tmp/pytest. No whole-project context or bind. Existing install layers were cached; no fresh dependency download is claimed. Build logs, test log, inspection JSON and signal result are under the new ignored staging only. Expected Linux warning: unknown cache_dir with disabled cacheprovider.

Runtime smoke commands use `docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev`, then `coworking-nearby:v2 python -m coworking_nearby.catalog`; synthetic adds `--mount type=bind,src=$PWD/examples,dst=/synthetic,readonly` before image and catalog path `/synthetic/coworkings.synthetic.json`. Blank startup adds `-e BOT_TOKEN=` before image. Detached start uses same restrictions plus `-d -e BOT_TOKEN=123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk`; wait for safe start, `docker stop --time 20 CONTAINER`, `docker inspect --format '{{.State.ExitCode}}' CONTAINER`, `docker logs CONTAINER`, `docker rm -f CONTAINER`. Python subprocess orchestration records real statuses/times. Initial smoke assertion mistakenly expected event/stage fields only; actual safe JSON also includes fixed generated id/count. Corrected harness verified all four keys, 32 lowercase hex id/count0 and exact event/stage sequence on fresh reruns; no product change was needed.

Actual runtime Python inspection enumerated /app files and distributions: exact nine package .py + requirements.lock + data/coworkings.json; every hash equals final host file, UID10001, catalog nonwritable, no .env/tests/devdeps/pytest/setuptools. Dev interpreter/distribution inventory also executed offline and confirms lock versions above. Final source/test SHA256:
- telegram_app.py: cc96cf1e6bdde223648bd2d8cf7f2f8dbba6027d62f72d389fc6e63d9c472ff8
- __main__.py: 5aa4e26f038d968a8f4856cb79aa6a41a16ab5e848a50e34758f945a01459d7d
- test_telegram_app.py: 60989e913dc215cc4685737c836efe69b6fe03da3fe2b16e4778878e8558d715
- test_privacy.py: ced3681d52c24f5a6dd9a8dd7cbc5e033f2142001a2254f44ea48bb1095c065c

Source/test writes now stopped. Documentation records observations after checks and is not installed in runtime. No new acceptance, live Telegram/URL guarantee, owner data, load/SLA, noncooperative-loop bound, historical RED certification or CI result follows. Repository remains unborn/no HEAD. All previously documented live/manual/platform limits remain. Parent must independently check and audit this new source.

## First-live ingress finding — narrow repair under RFC-001 (2026-10-19)

Generator: coder/coworking-20261019-01, sole C-coder. Only product writes: `coworking_nearby/telegram_app.py`, `tests/test_telegram_app.py`, `docs/verification.md`. Before writes, read AGENTS.md/coder TOML and ran `python3 .codex/forgeplan-pipeline.py status`: exit0, RFC-001/build/dev_unlocked=true, PRD-001. Scoped read-only MCP get independently confirmed active RFC/PRD/SPEC, RFC based_on PRD-001/SPEC-001, updated_at=2026-10-18T21:37:59.988494+00:00. Python hashlib of exact canonical MCP body matched e1ba834e4364dc5e2cb0bd31a88617e2ba6f661677cec85d058bacaf85bb9177. First shell hash attempt had a quoting parse error; corrected safely quoted Python command returned the matching hash. Scoped health returned needs_attention with advisory phase mismatches; no recommendations to score/mutate were executed.

Parent-supplied independent live diagnostic, NOT rerun or inspected by coder: getUpdates timeout1/clienttimeout3 failed with TelegramNetworkError/noHTTP after3.005s and3.006s; clienttimeout10 returned HTTP200/updates0 after6.181s. Parent reports bot stopped before diagnosis. These supplied observations motivate the virtual6s response; they are not coder live proof. RFC does not require clienttimeout3. Production diff versus frozen V2 staging is exactly ingress `request_timeout=3` -> `15`; polling timeout1/limit1, ordered cursor, backoff5, sendattempt10/service90/fullpause1.1/fullretry15, ingress cancel/join2 and cleanup coordinator remain unchanged. No spec divergence.

Actual RED before source fix:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_telegram_app.py::test_poll_six_second_response_and_prompt_shutdown
```
Observed **1 failed in2.42s**, then diagnostic assertion rerun **1 failed in2.36s**: processed=[], stop/ingress, one request, in backoff at virtual6. Fake get_updates uses actual `asyncio.timeout(request_timeout)` around virtual6s sleep. First fixed-code attempt exposed a harness error: emitter lambda rejected worker wait_ms keyword, yielding stop/worker; intermediate full run **706 passed/1 failed in10.43s**. Corrected recorder accepts kwargs and excludes queue events. Repeated actual old3 RED with corrected harness (`--tb=short`): **1 failed in2.30s**, same stop/ingress. Restored15, unchanged corrected test GREEN **1 passed in2.53s**. No fabricated historical RED. GREEN verifies processed update/cursor101 and second ordered poll, no ingress error, cancellation of that slow poll without advancing virtual time, two shutdown callers and subsequent shutdown retaining identical completed coordinator, ingress cancelled, pending0/workers0, elapsed virtual0<2. Existing stage deadline tests also run.

Final host commands, Python3.12.15/Clang23.1.3:
```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_telegram_app.py tests/test_privacy.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q
```
Observed exit0: **138 passed in7.11s**, then **707 passed in10.84s**, no skips. Autouse offline DNS/socket guard unchanged; all prior706 tests retained.

Container verification is **BLOCKED**, not green. Fresh ignored `.venv/verification/ingress-fix/stage.py` constructs explicit closed USTAR archives: runtime12 files (Dockerfile, requirements.lock, nine package .py, generated empty[] catalog); dev28 approved files (package/tests, blank .env.example, README, pyproject, both locks, production Dockerfile, compose, generated empty[] catalog, synthetic example, unchanged Dockerfile.test). Current working catalog check found **0 entries**, SHA2564f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945; it was not copied or changed. Stage generates [] regardless of working catalog. Exact pinned base and hash-enforced dependency instructions unchanged. No project-dot build or repository mount.

Using the required PATH prepend, isolated DOCKER_CONFIG=$PWD/.venv/verification/docker-config and DOCKER_HOST=unix:///Users/mxmknn/.docker/run/docker.sock:
```sh
docker build -f Dockerfile -t coworking-nearby:ingress-fix - < .venv/verification/ingress-fix/runtime.tar
docker build -f Dockerfile.test -t coworking-nearby:test-ingress-fix - < .venv/verification/ingress-fix/dev.tar
docker run --rm --network none --read-only --tmpfs /tmp:rw,nosuid,nodev coworking-nearby:test-ingress-fix
```
Both builds failed exit1: `permission denied while trying to connect to the docker API` at the required socket. Initial image inspect and test-run attempts also returned that error. Separate Python subprocess capture confirmed both exact build exit codes in ignored docker-attempts.json. The initial multiline shell's final cat returned0; that is NOT a build/test success. Session approval policy never forbids escalation; no bypass attempted. **No new image IDs available; Linux suite, runtime catalog/blank-token/UID/no.env/sourcehash/SIGTERM smokes remain UNPERFORMED for this repair.** Prior V2/local tags were not changed by these failed builds; their old IDs/results above are historical. Staging ready for authorized parent execution, not Linux proof.

Final host source SHA256: telegram_app.py **9ab5b1a3884acfed29894aa5b3dc6de4df86b1b4abac4ff4e21ab6f9a5cdaafd**; test_telegram_app.py **d842b462fd8b64a7ec917b0225f3747a32e3c4368ce88829d83e4d556bac0a6b**. Runtime sourcehash match cannot be claimed. No actual .env/token/private Docker config read/hash/consume; no live diagnostics, other bots, actual Telegram process, artifact/status/guard/role/pipeline/config/lock changes, commits, PRs or deployment. All child commands finished. These are C-coder observations with an explicit verification blocker, not independent PASS, Guardian PASS, manual routes acceptance or Ship authorization. Parent retains live ownership and independent review.
