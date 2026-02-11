# Beckn Implementation Guides – Markdoc Service

This repository contains the **Beckn Implementation Guide for EV Charging**
authored in Markdoc, and a reusable pipeline for Beckn-aligned implementation
guides for other networks.

The guide is composed from:

- A Beckn **Implementation Guide source document** (e.g.
  `EV_Charging.md` in the `beckn/DEG` repository), retrieved live from
  GitHub.
- **Local user stories and examples** (e.g. EV user journeys and JSON
  payloads), maintained in this repository.

The build process produces a single `index.md` file at the repo root. This is
the canonical Beckn Implementation Guide document for this repository, and a
GitHub Actions workflow keeps it up to date automatically.

---

## Repository layout

From the repo root:

```text
README.md                 # You are here: how things work and how to use them
.gitignore
.github/workflows/
  ev-docs-pages.yml       # GitHub Actions workflow that rebuilds docs/index.md

docs/
  index.md                # BUILT: composed Beckn Implementation Guide
  build/
    script.py             # Builder that performs the composition
    index.mdoc            # Markdoc entrypoint for the EV Charging guide
    adaptations/
      UserStories.md      # EV user stories and API examples (13.1, 13.2, ...)
```

### Source modules

- **`docs/build/index.mdoc`**
  - Markdoc entrypoint that defines *which* sections are composed into the
    Beckn Implementation Guide and in what order.
  - Uses custom tags:
    - `remote-section src="..." id="..."` – references a section by anchor id
      from a remote Markdown Implementation Guide document (for example,
      `EV_Charging.md`).
    - `local-section file="..." id="..."` – references a section by anchor id
      from a local Markdown file under `docs/build/adaptations/`.

- **`docs/build/adaptations/UserStories.md`**
  - Local content for the EV user stories and API examples (for example,
    the 13.1 and 13.2 workflows).
  - Contains `<span id="...">` anchors that correspond to the `id="..."`
    values used in `local-section` tags, allowing the builder to extract the
    relevant slices.

- **`docs/build/script.py`**
  - Python script that:
    1. Reads `docs/build/index.mdoc`.
    2. Resolves each `remote-section` by fetching the remote Markdown and using
       its table of contents to locate the requested section.
    3. Resolves each `local-section` by reading the local file and extracting
       the section starting at the matching anchor.
    4. Writes the final composed Markdown to `docs/index.md`.

### Generated artifacts and CI

- `docs/index.md` – generated output; overwritten by the builder.
- `.github/workflows/ev-docs-pages.yml` – CI pipeline; usually changed only
  when adjusting infrastructure.

---

## How the build & deploy pipeline works

### 1. Local build (for testing)

From the repo root:

```bash
pip install requests  # once

python docs/build/script.py docs/build/index.mdoc -o docs/index.md
```

This:
- Expands all `remote-section` and `local-section` tags.
- Writes the composed guide to `docs/index.md`.

You can then preview it locally via VS Code Markdown preview or with a simple
HTTP server:

```bash
python -m http.server 8000
# open http://localhost:8000/docs/index.md in a browser or Markdown viewer
```

### 2. CI auto-build of `docs/index.md`

The workflow in `.github/workflows/ev-docs-pages.yml` is wired to:

1. Run on pushes to `main` that touch the Markdoc sources or builder script
   under `docs/build/` (and on manual dispatch).
2. Install Python + `requests`.
3. Build `docs/index.md` from `docs/build/index.mdoc`:

   ```yaml
   - name: Build EV General Markdown
     run: |
       python docs/build/script.py docs/build/index.mdoc -o docs/index.md
   ```

4. If the regenerated `docs/index.md` differs from the committed version,
   commit the new file back to the repository.

This ensures `docs/index.md` is always in sync with the Markdoc sources
(`docs/build/`) on the `main` branch.

---

## Creating Beckn Implementation Guides for new networks

You can reuse this repository as a **reference implementation** for authoring
and publishing Beckn Implementation Guides for other networks.

1. **Fork or clone this repo.**

2. **Decide your Beckn Implementation Guide source document**
   - For example, if you publish a new Beckn Implementation Guide for a
     network at:
     - `https://raw.githubusercontent.com/your-org/specs/main/docs/MyNetwork_Implementation_Guide.md`

3. **Create a new Markdoc entrypoint** under `docs/build/`:

   ```bash
   cp docs/build/index.mdoc docs/build/my-network.mdoc
   ```

   Then edit `my-network.mdoc`:
   - Update the frontmatter title.
   - Replace `src="...EV_Charging.md"` URLs with the raw URL of your new
     Beckn Implementation Guide document.
   - Update the `id="..."` values to match the anchors in that document’s
     table of contents.

4. **Add or adapt local content under `docs/build/adaptations/`**
   - For example, create `docs/build/adaptations/MyNetworkUserStories.md` with your local
     journeys and examples.
   - Add `<span id="...">` anchors that you want to reference from
     `local-section` tags.
   - In your `.mdoc`, point to that file:

     ```md
     {% local-section
        file="adaptations/MyNetworkUserStories.md"
        id="101-example-1-some-user-story" %}
     {% /local-section %}
     ```

5. **Wire a build step for the new guide (optional)**
   - By default this setup builds `docs/build/index.mdoc` → `docs/index.md`.
   - If you want a separate entrypoint (e.g. `/my-network`), you can extend the
     workflow to build additional outputs (e.g. `my-network.md`) and add
     navigation in `index.md`.

---

## Structure and conventions

-- Source files for Beckn Implementation Guides are located under `docs/build/`.
- `remote-section` / `local-section` tags are expected to follow these
  conventions:
  - `src` / `file` values are URLs or paths relative to `docs/build/`.
  - `id` values correspond to anchors defined either in:
    - The upstream Implementation Guide’s table of contents (for remote
      sections), or
    - `<span id="...">` anchors in `docs/build/adaptations/*.md` files (for local sections).
- The builder can also be executed locally if required, via:

  ```bash
  python docs/build/script.py docs/build/index.mdoc -o docs/index.md
  ```

This setup is intended to be **clonable and extensible**: teams can fork this
repository, point `remote-section` tags at their own Beckn Implementation
Guide documents, add local user stories in `docs/build/adaptations/`, and
obtain an auto-generated Beckn Implementation Guide (`docs/index.md`) with
minimal effort.
