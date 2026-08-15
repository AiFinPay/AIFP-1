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

AIFP-1 и AIFP-2/x402 — разные экономические профили. **В AIFP-1 цена, которую видит и оплачивает агент, является gross-суммой. Из неё мерчант получает 99%, AiFinPay — 1%, creator/referral — 0%. Комиссия 1% не добавляется сверху.** AIFP-2/x402 — отдельный маршрут агентских платежей с профилем `0/0`.

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
  |<-- Quote {gross, merchant, fee, route} ----------|       |
  |                               |                          |
  |-- проверяет budget по gross                              |
  |-- подписывает/отправляет ровно gross своей wallet        |
  |-- POST /v1/pay {tx_ref, Idempotency-Key} ------>|        |
  |                               |                          |-- verify settlement + 99/1/0
  |<-- Receipt Token (JWT) --------------------------|       |
  |                               |                          |
  |-- GET /api/data ------------->|                          |
  |   Payment-Receipt: <JWT>      |                          |
  |                               |-- verify Ed25519         |
  |                               |-- check replay/quota     |
  |<-- 200 OK (данные) ----------|                          |
```

### Экономика binding quote

Для текущего AIFP-1 quote должен однозначно связывать:

```text
gross_amount = полная коммерческая сумма, которую платит агент
payer_total_amount = gross_amount
protocol_fee_amount = 1% от gross
creator_amount = 0
merchant_amount = gross_amount - protocol_fee_amount
merchant_amount + protocol_fee_amount + creator_amount = gross_amount
```

Пример Standard:

```json
{
  "gross_amount": "0.0005",
  "payer_total_amount": "0.0005",
  "merchant_amount": "0.000495",
  "protocol_fee_amount": "0.000005",
  "creator_amount": "0",
  "treasury_bps": 100,
  "creator_bps": 0
}
```

Для 6-decimal актива это `500 gross → 495 merchant + 5 AiFinPay` base units. Вариант `505 total → 500 merchant + 5 AiFinPay` является **fee-on-top и не соответствует текущему AIFP-1**.

### Ключевые концепции

| Концепция | Описание |
|---|---|
| **402 Payment Required** | HTTP-статус, который говорит «нужна оплата» |
| **Payment Challenge** | Машиночитаемый AIFP-1 challenge: мерчант, ресурс, pricing tier, quote endpoint и срок |
| **Quote** | Binding gross-цена и точный `99/1/0` split для конкретного ресурса/маршрута |
| **Receipt Token** | JWT, подписанный Ed25519 и выданный только после проверки settlement |
| **Stateless Verification** | Мерчант проверяет подпись receipt локально; replay/quota при необходимости остаются stateful |
| **Idempotency-Key** | Ключ для предотвращения повторной обработки одного settlement submission |

### Проверка receipt

1. **Signature** — Ed25519 через доверенные verification keys/JWKS (EdDSA only, `alg:none` запрещён)
2. **Issuer** — доверенный issuer
3. **Audience** — `aud == merchant_id`
4. **Resource** — receipt покрывает запрошенный resource/scope
5. **Amount / quota** — достаточно оплаченного gross/лимита; денежные значения сравниваются как Decimal/целые minor units, не float
6. **Expiry** — receipt не истёк согласно активному профилю
7. **Replay / quota state** — receipt не используется вне разрешённой модели повторного доступа/квоты

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

`max_price_usd` для AIFP-1 сравнивается с **gross payer amount**, а не с 99% merchant amount.

### Типы сообщений

| Тип | Кто отправляет | Что означает |
|---|---|---|
| **request** | Агент A → Агент B | «Сделай действие, я заплачу» |
| **challenge** | Агент B → Агент A | «Нужна оплата» (содержит AIFP-1 payment challenge) |
| **payment** | Агент A → Агент B | «Я заплатил, вот receipt» |
| **response** | Агент B → Агент A | «Вот результат работы» |
| **status** | Агент B → Агент A | Опциональное сообщение о прогрессе |

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
   |<-- Gross-inclusive Quote --------------|<--
   |                                        |
   |-- settle exactly gross from wallet     |
   |-- POST /v1/pay {tx_ref} -------------->|--> AiFinPay Gateway
   |<-- Receipt Token ----------------------|<--
   |                                        |
   |-- ACP Payment (receipt + request) ---->|
   |                                        |-- verify receipt
   |<-- ACP Response (результат) -----------|
```

Агент B может одновременно выступать и **агентом**, и **мерчантом**. Идентификаторы agent/merchant должны быть связаны явно и проверяемо; не следует предполагать их равенство без правила протокола.

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
| **Quote Service** | Выдаёт binding quote: gross, merchant amount, protocol fee, creator amount, expiry, asset, chain |
| **Settlement Verification** | Проверяет settlement и точный `payer=gross`, `merchant+fee+creator=gross` до выдачи receipt |
| **Receipt Authority** | Подписывает receipt Ed25519 после успешной settlement verification |
| **Ledger / Reconciliation** | Хранит и сверяет gross, merchant, AiFinPay fee, creator и settlement state |
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
| Transport | TLS согласно активной deployment/security policy |
| Nonce / payment ID | Достаточная уникальность и replay binding согласно активному профилю |
| Agent Passport | Отдельный AIFP-3 профиль, если используется |

### Защита от атак

| Атака | Защита |
|---|---|
| Forgery receipt | Ed25519 + контролируемая ротация ключей |
| Replay receipt | Nonce/payment identity/idempotency/replay state согласно типу receipt |
| Cross-resource reuse | `aud` + resource/scope binding |
| Double-processing | Idempotency-Key и уникальные settlement identifiers |
| Float bypass | Decimal/целые minor units, не float |
| Gross/net confusion | Явные gross/merchant/fee/creator поля + conservation check |
| Fee-on-top drift | Route отклоняется до оплаты, если payer total отличается от gross |
| Token decimals | Канонические decimals конкретного chain/asset |
| Webhook replay | Event ID tracking и signature verification |

---

## Pricing

| Tier | Gross платит агент | 99% мерчанту | 1% AiFinPay | Пример |
|---|---:|---:|---:|---|
| **Standard** | `$0.0005` | `$0.000495` | `$0.000005` | Простой read, одна запись |
| **Complex** | `$0.002` | `$0.00198` | `$0.00002` | Поиск, агрегация |
| **Premium** | `$0.005` | `$0.00495` | `$0.00005` | AI inference, GPU |

**Экономический профиль AIFP-1:** `treasuryBps = 100`, `creator/referralBps = 0`, settlement semantics = **gross-inclusive**. AiFinPay получает ровно 1% из gross успешной монетизированной транзакции, мерчант получает 99% до внешних network/settlement costs. **1% не добавляется сверху. AIFP-2/x402 — отдельный профиль `0/0` с 0% комиссии AiFinPay.**

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
