# Архитектура протокола AIFP-1

## Общее устройство

AIFP-1 — это протокол монетизации AI-трафика и платного доступа для AI-агентов, который использует HTTP `402 Payment Required` как сигнал необходимости оплаты.

```
┌─────────────────────────────────────────────────────┐
│          Внешний слой: HTTP 402 / AIFP-1           │
│  402 Challenge → Quote → Pay → Receipt → Retry      │
│  Агент ←→ Мерчант ←→ AiFinPay Gateway               │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│          Внутренний слой: ACP                        │
│  Агент A ←ACP→ Агент B ←ACP→ AiFinPay Backend       │
│  Агент A ←ACP→ Quote Service ←ACP→ Pay Engine       │
│  Pay Engine ←ACP→ Settlement ←ACP→ Ledger           │
└─────────────────────────────────────────────────────┘
```

AIFP-1 и AIFP-2/x402 — разные экономические профили. AIFP-1 монетизирует действия агента у мерчанта и использует профиль `100/0` (1% AiFinPay, 0% creator/referral). AIFP-2/x402 — отдельный маршрут агентских платежей с профилем `0/0`.

---

## Уровень 1: HTTP 402 / AIFP-1 (внешний)

Это протокол для взаимодействия **агент → мерчант**. Работает на HTTP `402 Payment Required` и собственном AIFP-1 challenge/quote/receipt flow.

### Полный цикл оплаты

```
Агент                          Мерчант                    AiFinPay
  |                               |                          |
  |-- GET /api/data ------------->|                          |
  |                               |-- проверка квоты         |
  |                               |-- квота закончилась      |
  |<-- 402 + AIFP-1 Challenge ----|                          |
  |                               |                          |
  |-- POST /v1/quote ------------------------------->|       |
  |<-- Quote {amount, nonce} -------------------------|       |
  |                               |                          |
  |-- подписывает/отправляет settlement своей wallet         |
  |-- POST /v1/pay {tx_ref, Idempotency-Key} ------>|        |
  |                               |                          |-- verify settlement
  |<-- Receipt Token (JWT) --------------------------|       |
  |                               |                          |
  |-- GET /api/data ------------->|                          |
  |   Payment-Receipt: <JWT>      |                          |
  |                               |-- verify Ed25519         |
  |                               |-- check nonce (atomic)   |
  |                               |-- consume nonce          |
  |<-- 200 OK (данные) ----------|                          |
```

### Ключевые концепции

| Концепция | Описание |
|---|---|
| **402 Payment Required** | HTTP-статус, который говорит «нужна оплата» |
| **Payment Challenge** | Машиночитаемый AIFP-1 challenge: куда платить, сколько, nonce, срок |
| **Quote** | Фиксированная цена на конкретный ресурс. Короткий TTL (300с) |
| **Receipt Token** | JWT, подписанный Ed25519. Содержит: iss, aud, resource, amount, nonce, exp |
| **Stateless Verification** | Мерчант проверяет receipt локально по подписи. **Не обращается к AiFinPay** для каждой проверки |
| **Nonce Store** | Атомарное хранилище nonce с TTL. Защита от replay |
| **Idempotency-Key** | UUID v4 в заголовке. Окно 24ч. Защита от двойной обработки |

### Проверка receipt

1. **Signature** — Ed25519 через JWKS (EdDSA only, `alg:none` запрещён)
2. **Issuer** — `iss == AiFinPay`
3. **Audience** — `aud == merchant_id`
4. **Resource** — receipt покрывает запрошенный resource/scope
5. **Amount / quota** — достаточно оплаченного лимита; денежные значения сравниваются как Decimal/целые minor units, не float
6. **Expiry** — `now < exp` с ограниченным clock skew
7. **Nonce / replay state** — receipt не должен быть использован вне разрешённой модели повторного доступа/квоты

Любая обязательная проверка не прошла → запрос отклоняется fail-closed.

---

## Уровень 2: ACP (внутренний)

Это протокол для структурированного взаимодействия **агент ↔ агент**. Он может переносить AIFP-1 payment challenge/receipt metadata, но не превращает AIFP-1 в x402.

### Формат сообщения

```json
{
  "acp_version": "1.0",
  "message_id": "msg_7f3a9c2e",
  "timestamp": "2026-07-24T12:00:00Z",
  "sender": {
    "agent_id": "agt_4f9a2c7e",
    "passport_id": "pp_2b9f8d1a",
    "signature": "ed25519:Base64UrlSignature"
  },
  "recipient": { "agent_id": "agt_8b3c1d5f" },
  "type": "request",
  "payload": {
    "action": "search",
    "resource": "/api/company?q=Acme",
    "pricing_tier": "complex",
    "max_price_usd": "0.005"
  }
}
```

### Типы сообщений

| Тип | Кто отправляет | Что означает |
|---|---|---|
| **request** | Агент A → Агент B | «Сделай действие, я заплачу» |
| **challenge** | Агент B → Агент A | «Нужна оплата» (содержит AIFP-1 payment challenge) |
| **payment** | Агент A → Агент B | «Я заплатил, вот receipt» |
| **response** | Агент B → Агент A | «Вот результат работы» |
| **status** | Агент B → Агент A | «Прогресс 45%, осталось 15с» (опционально) |

### Cross-agent payment flow

```
Агент A (плательщик)              Агент B (исполнитель)
   |                                        |
   |-- ACP Request (action, resource) ----->|
   |                                        |-- проверка квоты
   |                                        |-- требуется оплата
   |<-- ACP Challenge (AIFP-1 payload) -----|
   |                                        |
   |-- POST /v1/quote --------------------->|--> AiFinPay Gateway
   |<-- Quote ------------------------------|<--
   |                                        |
   |-- settle from agent wallet             |
   |-- POST /v1/pay {tx_ref} -------------->|--> AiFinPay Gateway
   |<-- Receipt Token ----------------------|<--
   |                                        |
   |-- ACP Payment (receipt + request) ---->|
   |                                        |-- verify receipt
   |<-- ACP Response (результат) -----------|
```

Агент B может одновременно выступать и **агентом**, и **мерчантом**. Идентификаторы agent/merchant должны быть связаны явно и проверяемо; не следует предполагать их равенство без правила протокола.

### Discovery

Каждый агент, принимающий ACP, может публиковать machine-readable discovery document:

```
GET /.well-known/agent.json
```

Пример:

```json
{
  "acp_version": "1.0",
  "agent_id": "agt_8b3c1d5f",
  "public_key": "ed25519:Base58PubKey",
  "capabilities": [
    {
      "action": "search",
      "pricing_tiers": ["standard", "complex"],
      "max_price_usd": "0.005",
      "accepted_assets": ["USDC", "USDT"],
      "accepted_chains": ["polygon", "base"]
    }
  ],
  "free_quota": 100
}
```

### Транспорты

| Транспорт | Для чего |
|---|---|
| **HTTP POST** | Запрос/ответ через обычный HTTP |
| **WebSocket** | Двунаправленный стрим для долгих задач |
| **SSE** | Прогресс-уведомления от сервера к клиенту |
| **P2P (libp2p)** | Возможный прямой агент↔агент транспорт; требует отдельной реализации/проверки |

---

## Внутренний бэкэнд AiFinPay

Логически AIFP-1 включает сервисы quote, settlement verification, receipt issuance, ledger/reconciliation и merchant integration. Конкретная production-топология является реализационной деталью, а не гарантией протокола.

```
┌────────────────────────────────────────────────┐
│              AiFinPay Control Plane             │
│                                                 │
│  Quote Service ←→ Settlement Verification      │
│       ↓                    ↓                    │
│  Receipt Authority ←→ Ledger/Reconciliation    │
│       ↓                    ↓                    │
│  JWKS Service          Webhook Service          │
└────────────────────────────────────────────────┘
```

| Сервис | Что делает |
|---|---|
| **Quote Service** | Выдаёт binding quote: price, nonce, expiry, asset, chain |
| **Settlement Verification** | Проверяет settlement, выполненный кошельком агента, перед выдачей receipt |
| **Receipt Authority** | Подписывает receipt Ed25519 |
| **Ledger / Reconciliation** | Хранит и сверяет финансовые события и settlement state |
| **JWKS Service** | Публикует публичные ключи для верификации |
| **Webhook Service** | Уведомляет мерчантов о lifecycle событиях |

### State machine транзакции

```
QuoteRequested → QuoteIssued → PaymentObserved → PaymentVerified → ReceiptIssued
```

Точные finality requirements зависят от сети, актива и risk policy реализации и должны быть определены в deployment/runbook для соответствующего settlement route.

---

## Безопасность

### Криптография

| Назначение | Алгоритм / правило |
|---|---|
| Подпись receipt | EdDSA / Ed25519 |
| Подпись webhook | HMAC-SHA256 |
| Transport | TLS |
| Nonce | CSPRNG ≥ 128 бит |
| Agent Passport | Ed25519, если используется соответствующий профиль |

### Защита от атак

| Атака | Защита |
|---|---|
| Forgery receipt | Ed25519 + контролируемая ротация ключей |
| Replay receipt | Nonce/idempotency/replay state согласно типу receipt |
| Cross-resource reuse | `aud` + resource/scope binding |
| Double-processing | Idempotency-Key и уникальные settlement identifiers |
| Float bypass | Decimal/целые minor units, не float |
| JWKS DoS | Cache/backoff/rotation policy |
| Clock skew | Ограниченный tolerance |
| Webhook replay | Event ID tracking и signature verification |

---

## Pricing

| Tier | Минимум | Пример |
|---|---|---|
| **Standard** | $0.0005 | Простой read, одна запись |
| **Complex** | $0.002 | Поиск, агрегация |
| **Premium** | $0.005 | AI inference, GPU |

**Экономический профиль AIFP-1:** `treasuryBps = 100`, `creator/referralBps = 0`. AiFinPay получает ровно 1% успешной монетизированной транзакции, мерчант получает 99% до внешних network/settlement costs. **AIFP-2/x402 — отдельный профиль `0/0` с 0% комиссии AiFinPay.**

---

## Файлы протокола

| Документ | Что описывает |
|---|---|
| **Doc 01** — RFC | Нормативная спецификация AIFP-1 |
| **Doc 02** — Merchant Guide | Интеграция мерчанта |
| **Doc 03** — Agent SDK Spec | Поведение агента, бюджеты и payment flow |
| **Doc 04** — Security Spec | Threat model и криптографические требования |
| **Doc 08** — OpenAPI 3.1 | Machine-readable API контракт |
| **Doc 10** — JSON Schemas | Форматы объектов |
| **Doc 16** — ACP Spec | Агент↔агент коммуникация |
