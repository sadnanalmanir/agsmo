# Automated GitHub Pages documentation (WIDOCO + LODE)

## Answer: yes, this is automatable

You do **not** need to click through LODE or WIDOCO by hand for every release.
The standard pattern for ontology repos is:

```
push ontology change → GitHub Actions → WIDOCO (uses LODE internally)
  → static HTML site → GitHub Pages
```

After that, **w3id.org** can permanently redirect `https://w3id.org/agsmo/...` to the Pages URL.

## LODE vs WIDOCO vs OnToology

| Tool | Role | Fit for automation |
|------|------|--------------------|
| **[LODE](https://lode.opencitations.net/)** | Renders classes/properties as HTML (term reference) | Web service / library; awkward alone for full site |
| **[WIDOCO](https://github.com/dgarijo/Widoco)** | Full doc wizard: **embeds LODE**, metadata, WebVOWL, sections, provenance options | **Best for CI**: JAR or Docker, CLI flags |
| **[OnToology](https://ontoology.linkeddata.es/)** | GitHub app/service that runs Widoco on push | Zero workflow file, but external dependency + setup |

**Recommendation for `sadnanalmanir/agsmo`:** GitHub Actions + WIDOCO JAR (what this repo implements).  
LODE is still “in the stack” — WIDOCO calls that stack for the cross-reference section. You do not need a separate LODE step.

## What we automated

Workflow: [`.github/workflows/publish-docs.yml`](../.github/workflows/publish-docs.yml)

| Trigger | Effect |
|---------|--------|
| Push to `main` changing `ontology/**` | Rebuild + redeploy docs |
| Manual **Actions → Publish ontology documentation → Run** | Same |

**Pipeline steps:**

1. Checkout repo  
2. Install Java 17  
3. Download WIDOCO release JAR  
4. Run WIDOCO on `ontology/agsmo.ttl`  
5. Upload `site/` as Pages artifact  
6. Deploy with official `actions/deploy-pages`

**Site URL (after first successful run):**  
https://sadnanalmanir.github.io/agsmo/

## One-time GitHub settings (required)

1. Repo **Settings → Pages**  
2. **Source:** GitHub Actions (not “Deploy from a branch”)  
3. First workflow run must succeed (permissions already set in the YAML: `pages: write`, `id-token: write`)

If Pages is not enabled, the deploy job fails until you switch the source to Actions.

Optional via CLI (owner only):

```bash
gh api -X POST repos/sadnanalmanir/agsmo/pages \
  -f build_type=workflow
```

## Local regeneration (optional)

```bash
# Requires Java 17+
curl -fsSL -o widoco.jar \
  https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-17.jar

java -jar widoco.jar \
  -ontFile ontology/agsmo.ttl \
  -outFolder site \
  -getOntologyMetadata \
  -webVowl \
  -rewriteAll \
  -uniteSections \
  -lang en \
  -includeAnnotationProperties \
  -noPlaceHolderText
```

## Improving how docs look

WIDOCO reads **ontology annotations** (Dublin Core, `rdfs:label`, `rdfs:comment`, `vann:`, etc.).  
Richer TTL metadata → richer HTML. See:

- [WIDOCO metadata guide](https://github.com/dgarijo/Widoco/blob/master/doc/metadataGuide/guide.md)  
- [Best practices](https://dgarijo.github.io/Widoco/doc/bestPractices/index-en.html)  
- Optional: [`widoco/config.properties`](../widoco/config.properties) (pass `-confFile` if you prefer config over pure TTL)

## After Pages works: w3id redirects

Once https://sadnanalmanir.github.io/agsmo/ is live:

1. PR to [perma-id/w3id.org](https://github.com/perma-id/w3id.org) claiming `agsmo/`  
2. `.htaccess` redirects permanent IRIs to Pages (and/or raw `.ttl`)  
3. Ontology IRIs (`https://w3id.org/agsmo/ns#`) become resolvable  

Do **not** register w3id before the Pages site exists.

## Limits of GitHub Pages

| Feature | On GitHub Pages |
|---------|------------------|
| HTML docs | Yes |
| WebVOWL diagram | Yes (client-side) |
| Apache `.htaccess` content negotiation | **No** (static hosting) |
| True `Accept: text/turtle` negotiation | Do via **w3id** or a small custom server later |

So: **pretty docs on Pages**; **content negotiation on w3id** (next step).
