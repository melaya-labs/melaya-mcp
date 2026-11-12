# Push review checklist

## Blast radius tiers

| Tier | Typical files | Consequence |
|---|---|---|
| Critical | shared contracts and types, database schema and migrations, auth, row-level security, the agent runner protocol, deploy scripts, tool manifests | significant change: security review before the base push |
| High | a service used by several products, environment keys, version pins, the prerender and SEO layer (canonical, hreflang, sitemap), i18n namespaces | quality go before the base push |
| Medium | one service's internals, a helper | normal review |
| Low | one UI component, tests, docs | normal review |

## Security

- Secrets scan covers added and deleted lines (deletion hunks carry the full old content).
- No credential, token, internal hostname, IP or personal data in code, tests, fixtures or commit messages.
- New service-to-service calls carry the internal authentication the architecture requires.
- New token parsers use the shared verifier, not a local copy.
- New dependencies: name, version, licence, and a dependency advisory lookup (hand to the CISO).
- CI actions pinned by commit and third-party images by digest.

## Tests

- Every behaviour change has a covering test, seen failing first.
- No test deleted without the code it covered.
- Auth, payment and approval paths: one test per changed branch.
- The project's full suite ran, not only the new file.

## Breaking changes

- Migration: timestamped, with a down file; the server tolerates it being absent so code and schema ship in either order.
- Environment: new keys documented in the deploy runbook, staged by the owner, never committed.
- Version pins: every place that names a released version agrees, and the release resolves before the pins deploy.
- Strings: present in every shipped locale, sanitizer passes (no em or en dashes).
- Public pages: exactly one canonical and at least one structured data block per route.
- API contracts: no removed field or changed type without a version or a migration path.

## Order

- Client-only commits do not force a server restart.
- A change that needs a native or engine symbol ships with that commit in the same push.
- Note the CI jobs needed and their order from the deploy runbook.

## Labels

- must: blocks the push.
- should: fix now unless the owner accepts the risk.
- nit: style, optional.
- question: needs an answer before the verdict.
