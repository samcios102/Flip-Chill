// BEST46 — Slack / Marketing counts toward 50k / 100k thresholds.
// Source affects the payout model, not threshold eligibility.

// Canonical portfolio source.
// item.source = item.source === "slack" ? "marketing" : (item.source || "cold");

// Portfolio -> settlement synchronization must preserve source:
// existing.source = item.source || existing.source || "cold";
// new record source = item.source || "cold";

// Threshold rule remains based on full net transaction revenue regardless of source:
// if (thresholdRevenue >= 50000) bonus = 5;
// if (thresholdRevenue >= 100000) bonus = 10;
// This includes cold, referral and Slack / Marketing transactions.

// BEST46 also exposes `Źródło` in the expanded Base apartment editor:
// Standard / zimny | Polecenie | Slack / Marketing
