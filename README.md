URL SHORTENER

## What it does (the basic idea)

You give it a long URL: `https://example.com/some/really/long/path?with=lots&of=params`
It gives you back something short: `https://yourdomain.com/aZ9k2`

Anyone who visits `yourdomain.com/aZ9k2` gets automatically sent to the original long URL. That's the entire product. Everything else (click tracking, expiry, custom slugs) is a feature layered on top of that one core behavior.

## How it works, step by step

**Step 1: Shortening a URL**
1. You send a `POST /shorten` request with the long URL in the body.
2. The server validates it — is this actually a well-formed URL? (Pydantic handles this.)
3. The server generates a short, unique identifier — the "slug" (e.g. `aZ9k2`). This is the interesting part, more below.
4. The server stores a row in the database: `{slug: "aZ9k2", original_url: "https://example.com/...", created_at: now, click_count: 0}`.
5. The server responds with the full short URL: `https://yourdomain.com/aZ9k2`.

**Step 2: Using a short URL**
1. Someone visits `yourdomain.com/aZ9k2` in their browser.
2. This hits your `GET /{slug}` route.
3. The server looks up `aZ9k2` in the database, finds the matching `original_url`.
4. The server increments `click_count` for that row.
5. The server responds with an HTTP redirect (a 302 response with a `Location` header pointing to the original URL).
6. The browser automatically follows that redirect — the user never sees your domain, they just land on the original page.

That lookup in step 3 is the crux of the whole system, and it's why the DSA connection matters.

## Why it's designed this way
**Why a slug and not just storing the whole URL as the "key"?**
You need something short and shareable. The slug is essentially a compressed, unique reference to a much longer string. This is exactly what a hash function or an ID-to-key mapping is for.

**Why is the lookup fast (O(1))?**
Because `slug` is typically the primary key or has a unique index on it. Database indexes are B+ trees or hash indexes — either way, looking up a single slug doesn't mean scanning every row in the table. It's a near-instant lookup regardless of whether you have 100 URLs or 100 million. This matters because the redirect endpoint is the one that gets hit *constantly* — way more than the "create" endpoint — so it has to be fast.

**Why generate the slug two different ways (base62 counter vs. hash)?**

- **Base62 encoding of an auto-incrementing counter**: Every new URL gets `id = 1, 2, 3...` from the database, and you encode that number using 62 characters (a-z, A-Z, 0-9) instead of just 10 digits. This makes short codes without collisions *by construction* — you literally can't have two URLs with the same ID. Downside: slugs are predictable and sequential (`aZ9k2` might reveal you're the 4,000,001st URL created), and it ties your slug generation to a single incrementing counter, which can be awkward in distributed systems (multiple servers can't agree on "the next number" without coordination).

- **Truncated hash (e.g. first 7 chars of MD5 of the URL)**: You hash the input URL itself. Same URL in → same hash out, which means duplicate submissions of the same URL can reuse the same slug (a nice bonus). Downside: collisions are possible — two *different* URLs could theoretically hash to the same truncated value, so you need a strategy for that (check if the slug's taken, and if so, re-hash with a salt or extend the truncation length).

This is why the roadmap has you implement both — it's a real, small-scale version of a system design tradeoff (predictability + coordination vs. collision handling), not just busywork.

**Why track clicks the way it does?**
Every redirect is an opportunity to record data cheaply — you're already loading that row to get the `original_url`, so incrementing a counter on it costs almost nothing extra. This is why click tracking is bundled into the redirect handler rather than being a separate system.

**Why 302 instead of 301 for the redirect?**
A 301 (permanent redirect) tells the browser "cache this — next time, don't even ask the server, just go straight to the destination." That breaks your click tracking, since repeat visits from the same browser will skip your server entirely after the first hit. A 302 (temporary redirect) forces the browser to check with your server every single time, which is what you want if click analytics matter to you.

**Why does expiry exist?**
Without it, your table grows forever and you're serving redirects for links nobody's used in years. A `expires_at` column, checked at lookup time, lets you either reject the redirect (link's dead) or clean up old rows in the background — keeping the table lean and the index fast.

My takeaway:
A user visits my website with a unique url that has a unique ID(slug) at the tail, i fund their website using that slug and return it to them.


## Known Issues / Technical Debt

### `expires_at` column type (VARCHAR instead of TIMESTAMP)

While building out the routes, a migration issue led to converting the
`expires_at` column from a timestamp type to `VARCHAR`. This was a
reactive fix to unblock a migration error rather than a deliberate
design choice, and it comes with real tradeoffs:

- **What still works:** existing values remain valid ISO 8601 strings,
  and reading/writing expiry dates through the API continues to work
  as long as the format stays consistent.
- **What's broken as a result:** SQL-level date comparisons
  (e.g. `WHERE expires_at < NOW()`) won't work correctly against a
  string column. Sorting by expiry date isn't guaranteed to match
  chronological order. Schema-level validation of the field is weaker,
  since Pydantic can't enforce "this must be a real datetime" as
  strictly against a string-backed column.
- **What this blocks going forward:** any feature involving expiry
  logic — auto-deleting expired links, filtering "active" vs.
  "expired" URLs, sorting by expiry — will require fixing this first.
  The correct fix is a new Alembic migration that casts the column
  back to `TIMESTAMP WITH TIME ZONE` using an explicit `USING`
  clause, handling existing NULL values gracefully.

This is being left as-is for now since Project 1 doesn't currently
implement expiry-based logic, but it's flagged here as debt to
revisit before any such feature is built.