# Архитектура протокола AIFP-1

## Общее устройство

AIFP-1 — это платёжный протокол для AI-агентов, который работает на **двух уровнях**:

```
┌─────────────────────────────────────────────────────┐
│          Внешний слой: HTTP + x402                  │
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

---

## Уровень 1: HTTP + x402 (внешний)

Это протокол для взаимодействия **агент → мерчант**. Работает на чистом HTTP.

### Полный цикл оплаты

```
Агент                          Мерчант                    AiFinPay
  |                               |                          |
  |-- GET /api/data ------------->|                          |
  |                               |-- проверка квоты         |
  |                               |-- квота закончилась      |
  |<-- 402 + Challenge -----------|                          |
  |                               |                          |
  |-- POST /v1/quote ------------------------------->|       |
  |<-- Quote {amount, nonce} -------------------------|       |
  |                               |                          |
  |-- POST /v1/pay {Idempotency-Key} -------------->|        |
  |                               |                          |-- списание
  |                               |                          |-- settlement
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
| **402 Payment Required** | HTTP-статус, который говорит «нужна оплата». Активирован из резерва HTTP/1.1 |
| **Payment Challenge** | JSON в теле 402: куда платить, сколько, nonce, срок |
| **Quote** | Фиксированная цена на конкретный ресурс. Короткий TTL (300с) |
| **Receipt Token** | JWT, подписанный Ed25519. Содержит: iss, aud, resource, amount, nonce, exp |
| **Stateless Verification** | Мерчант проверяет receipt локально по подписи. **Не обращается к AiFinPay** |
| **Nonce Store** | Redis SET NX EX. Атомарная операция. TTL = 600с. Защита от replay |
| **Idempotency-Key** | UUID v4 в заголовке. Окно 24ч. Защита от двойного списания |

### Почему stateless verification — это главное решение

Ed25519 верификация ≈ **50,000 операций/сек на ядро**. Мерчант не зависит от доступности AiFinPay. Даже если бэкэнд AiFinPay упал, уже выданные receipts продолжают работать до истечения TTL.

### Часы проверки receipt

1. **Signature** — Ed25519 через JWKS (EdDSA only, alg:none запрещён)
2. **Issuer** — iss == AiFinPay
3. **Audience** — aud == merchant_id
4. **Resource** — resource == запрошенный путь
5. **Amount** — amount >= required_price (Decimal, НЕ float!)
6. **Expiry** — now < exp (skew ≤ 5с)
7. **Nonce** — не использован (atomic SET NX EX)

Любая проверка не прошла → конкретный HTTP-статус (402/403/409/422).

---

## Уровень 2: ACP (внутренний)

Это протокол для взаимодействия **агент ↔ агент**. Структурированные JSON-сообщения, не HTTP-запросы.

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
| **challenge** | Агент B → Агент A | «Квота закончилась, заплати» (содержит x402 challenge) |
| **payment** | Агент A → Агент B | «Я заплатил, вот receipt» |
| **response** | Агент B → Агент A | «Вот результат работы» |
| **status** | Агент B → Агент A | «Прогресс 45%, осталось 15с» (опционально) |

### Cross-agent payment flow

```
Агент A (плательщик)              Агент B (исполнитель)
   |                                        |
   |-- ACP Request (action, resource) ----->|
   |                                        |-- проверка квоты
   |                                        |-- квота закончилась
   |<-- ACP Challenge (x402 payload) -------|
   |                                        |
   |-- POST /v1/quote --------------------->|--> AiFinpay Gateway
   |<-- Quote ------------------------------|<--
   |                                        |
   |-- POST /v1/pay ----------------------->|--> AiFinpay Gateway
   |    (Idempotency-Key)                   |
   |<-- Receipt Token ----------------------|<--
   |                                        |
   |-- ACP Payment (receipt + request) ---->|
   |                                        |-- verify receipt (Ed25519)
   |                                        |-- consume nonce (atomic)
   |<-- ACP Response (результат) -----------|
```

Агент B одновременно выступает и **агентом** (как клиент AiFinPay), и **мерчантом** (принимает оплату от A). Его `agent_id` = `merchant_id` в receipt.

### Discovery

Каждый агент, принимающий ACP, обязан отвечать на:

```
GET /.well-known/agent.json
```

Ответ:

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
| **P2P (libp2p)** | Прямое агент↔агент без инфраструктуры |

---

## Внутренний бэкэнд AiFinPay

Бэкэнд AiFinPay состоит из микросервисов, общающихся через ACP:

```
┌────────────────────────────────────────────────┐
│              AiFinPay Control Plane             │
│                                                 │
│  Quote Service ←ACP→ Pay Engine                │
│       ↓                    ↓                    │
│  Settlement Adapter ←ACP→ Receipt Authority    │
│       ↓                    ↓                    │
│  Blockchain/Fiat Rails   Ledger                 │
│                                                 │
│  JWKS Service ←→ Key Rotation (HSM/KMS)        │
│  Webhook Service ←→ Merchant Endpoints         │
│  Passport Service ←→ Agent Identity             │
└────────────────────────────────────────────────┘
```

| Сервис | Что делает |
|---|---|
| **Quote Service** | Выдаёт binding quote: price, nonce, expiry, asset, chain |
| **Pay Engine** | Списывает средства с кошелька агента, атомарно |
| **Settlement Adapter** | Переводит средства мерчанту (stablecoin или fiat) |
| **Receipt Authority** | Подписывает receipt Ed25519 ключом (HSM) |
| **Ledger** | Append-only журнал всех транзакций |
| **JWKS Service** | Публикует публичные ключи для верификации |
| **Webhook Service** | Уведомляет мерчантов о lifecycle событиях |
| **Passport Service** | Выдаёт и верифицирует Agent Passport |

### State machine транзакции

```
QuoteRequested → QuoteIssued → PaymentInitiated → PaymentSettled → ReceiptIssued
```

### Settlement tiers

| Tier | Подтверждения | Когда receipt = 200 |
|---|---|---|
| **Tier 1** (низкий риск) | 0 confirmations | Мгновенно |
| **Tier 2** (средний) | 1-3 blocks | После 1 подтверждения |
| **Tier 3** (высокий) | 3-6 blocks | Async: 202 → 425 → 200 |

Если failure rate > 1% за час → circuit breaker → все fallback на async (425).

---

## Безопасность

### Криптография

| Назначение | Алгоритм |
|---|---|
| Подпись receipt | EdDSA / Ed25519 |
| Подпись webhook | HMAC-SHA256 |
| Transport | TLS 1.3 |
| API ключи (at rest) | Argon2id |
| Nonce | CSPRNG ≥ 128 бит |
| Agent Passport | Ed25519 |

### Защита от атак

| Атака | Защита |
|---|---|
| Forgery receipt | Ed25519, ключ в HSM |
| Replay receipt | Nonce store (SET NX EX), linearizable |
| Cross-resource reuse | aud + resource binding |
| Double-spend | Idempotency-Key (24ч окно) |
| Float bypass | Decimal сравнение, НЕ float |
| JWKS DoS | Backoff + jitter, CDN cache, kid regex |
| Clock skew | Tolerance ≤ 5с |
| Webhook replay | Event ID tracking (TTL ≥ 24ч) |

---

## Pricing

| Tier | Минимум | Пример |
|---|---|---|
| **Standard** | $0.0005 | Простой read, одна запись |
| **Complex** | $0.002 | Поиск, агрегация |
| **Premium** | $0.005 | AI inference, GPU |

**Комиссия AiFinPay:** 1% начисляется сверху суммы мерчанта. Мерчант получает указанную сумму полностью (минус network costs).

---

## Файлы протокола

| Документ | Что описывает |
|---|---|
| **Doc 01** — RFC | Нормативная спецификация (25 секций) |
| **Doc 02** — Merchant Guide | Интеграция на 15 фреймворках |
| **Doc 03** — Agent SDK Spec | Авто-оплата, кошельки, бюджеты |
| **Doc 04** — Security Spec | Threat model, крипто, compliance |
| **Doc 08** — OpenAPI 3.1 | Machine-readable API контракт |
| **Doc 10** — JSON Schemas | Форматы всех объектов |
| **Doc 16** — ACP Spec | Агент↔агент коммуникация |
