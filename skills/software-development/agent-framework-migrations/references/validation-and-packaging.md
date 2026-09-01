# Validation and Packaging of Migrated Agent Kits

Use this after the semantic rewrite is complete. The goal is to prove that the destination package is internally coherent and safe to install—not merely that source product names disappeared.

## 1. Static validation

Build a deterministic validator that walks every text artifact and checks:

- source-runtime commands and config paths are absent outside an explicitly allowed migration/history document;
- every `SKILL.md` has parseable YAML frontmatter, a matching directory/name, a non-empty description/body, and destination size limits;
- every JSON fixture parses;
- relative Markdown links resolve from the containing file;
- renamed files are reflected in indexes, registries, templates, and lesson links;
- binary files are inventoried rather than decoded as text.

### False-positive trap

A validator that contains its own banned literals will flag itself. Exempt only the validator source and narrowly named migration/history documents, or store the patterns in an encoded/assembled form. Never exempt broad directories. The migration guide may cite old paths to explain their replacement; operational docs may not depend on them.

Regex-only frontmatter checks are an early smoke test, not final proof. Parse YAML when a parser is available.

## 2. Isolated installation test

Never test a starter-kit installer against the user's live profile. Point it at a fresh temporary home:

```bash
TEST_HOME="$(mktemp -d)"
HERMES_HOME="$TEST_HOME" bash scripts/install.sh
```

Then verify:

- the exact expected number of skill directories was installed;
- every installed directory contains `SKILL.md` and support files;
- frontmatter `name` matches the installed directory;
- no config, identity, memory, credential, or unrelated profile file was created;
- the live profile remains untouched.

Run the installer a second time against the same temporary home. A safe default should skip existing skills and report zero overwrites. Test any force mode separately and require timestamped backups before replacement.

If the destination CLI exists, run its native skill/config/doctor checks in the isolated environment. If it is unavailable, report that boundary and do not claim native validation.

## 3. Archive verification

Package with one stable top-level directory. Produce the requested format and, when useful, a broadly portable ZIP as an alternative. Reopen each archive after creation and assert:

- expected entry count;
- every entry is rooted under the intended top-level directory;
- required entry point, installer, validator, skills, and references are present;
- no temporary test home, cache, original source archive, or generated secret is included.

Compute checksums and sizes only after successful readback. Deliver the artifacts, hashes, validation summary, and the exact first-run commands.

## 4. Completion report

State separately:

1. semantic conversion performed;
2. files intentionally removed, renamed, preserved, and added;
3. static validation result;
4. isolated first-install and second-run/idempotency result;
5. native destination CLI result or explicit verification boundary;
6. archive readback count, size, and checksum.

Do not collapse these into “everything works”; each proves a different property.
