# Platform compatibility

What the current skill and plugin specifications actually allow, and what that forces on the design of a Shopify peak-season toolkit.

**Date checked: 21 September 2026.** Every claim carries a source. Claims that could not be verified from primary documentation are listed in section 9 rather than stated as fact.

---

## 1. Open Agent Skills: there is a cross-vendor standard

**Spec:** https://agentskills.io/specification · **Repo:** https://github.com/agentskills/agentskills

Originally developed by Anthropic and released as an open standard. Code is Apache-2.0, docs CC-BY-4.0.

**Layout:** `skill-name/SKILL.md` is required. `scripts/`, `references/` and `assets/` are optional conventions. Any other files are permitted.

**Frontmatter:**

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | 64 chars max, lowercase `a-z0-9` and hyphens, no leading or trailing hyphen, no `--`, and it must match the parent directory name |
| `description` | Yes | 1024 chars max, must say what it does **and** when to use it |
| `license` | No | License name or bundled file reference |
| `compatibility` | No | 500 chars max, environment requirements |
| `metadata` | No | Map of string to string |
| `allowed-tools` | No | Space-separated string. Marked experimental, support varies between implementations |

**Budget:** metadata around 100 tokens is always loaded; the SKILL.md body is recommended under 5,000 tokens and under 500 lines; everything else loads on demand.

**Validator:** `skills-ref validate ./my-skill`.

**Adoption:** roughly 45 clients listed at https://agentskills.io/clients, including Claude Code, ChatGPT and Codex, Cursor, VS Code and Copilot, Gemini CLI, Goose, OpenCode, Databricks and Snowflake Cortex.

**Governance caveat.** The repo has no releases or tags, the spec page carries no version number, and CONTRIBUTING.md states that proposals are reviewed by Anthropic and that major architectural changes are not being accepted. It is an open specification under single-vendor stewardship, not a foundation standard. Skill-level versioning is convention only, a free-text `metadata.version`.

### Agent Plugins 1.0.0, a separate and differently governed thing

https://agent-plugins.org/specification. A vendor-neutral standard for packaging skills **and** MCP servers into portable plugins. Technical steering committee: Amazon, Cursor, Microsoft, OpenAI, Vercel. **Anthropic is not on it.**

Layout: root `plugin.json` (`$schema` and `name` required), `skills/<name>/SKILL.md`, `mcp.json`, and reverse-domain extension directories. SemVer recommended.

---

## 2. OpenAI

**Canonical doc:** https://learn.chatgpt.com/docs/build-skills. The older `developers.openai.com/codex/*` URLs now redirect there.

OpenAI follows the open standard verbatim, plus one optional OpenAI-only file, `agents/openai.yaml`, carrying display metadata, an `allow_implicit_invocation` policy flag and MCP tool dependencies.

**Discovery order in Codex:** `$CWD/.agents/skills` → `$REPO_ROOT/.agents/skills` → `$HOME/.agents/skills` → `/etc/codex/skills` → bundled.

**Invocation:** `@skill` in ChatGPT, `$skill` in Codex CLI, plus implicit selection.

**The one published size limit:** the initial skills list is capped at 2% of the model's context window, or 8,000 characters when the window is unknown. Descriptions truncate first and excess skills are dropped with a warning. Once a skill is selected the full SKILL.md loads regardless.

**Surfaces:** standalone skills reach the ChatGPT desktop app, Codex CLI and the IDE extension. Skills bundled inside a plugin additionally reach ChatGPT web, mobile and Work. Standalone skills do not appear in ChatGPT web chat.

**Plugins** (https://developers.openai.com/plugins/build/plugins) use the agent-plugins.org 1.0.0 schema at the root, with OpenAI settings under `extensions.com.openai`. Local marketplaces live at `$REPO_ROOT/.agents/plugins/marketplace.json` or `~/.agents/plugins/marketplace.json`.

**Not to be confused with skills:** GPT Actions belong to custom GPTs, which are being retired (see uncertainties). The Apps SDK is MCP-based and builds UI inside ChatGPT. AGENTS.md is plain repo instructions with no frontmatter, stewarded by the Agentic AI Foundation, and is complementary rather than a skills format.

---

## 3. Claude Code

**Skills:** https://code.claude.com/docs/en/skills

Locations: `~/.claude/skills/<name>/SKILL.md` personal, `.claude/skills/` project, `<subdir>/.claude/skills/` nested, and `<plugin>/skills/<name>/SKILL.md` invoked as `/plugin-name:skill-name`.

Frontmatter is a **superset** of the open spec, adding `disable-model-invocation`, `user-invocable`, `context: fork`, `agent`, `arguments`, `argument-hint`, `model`, `effort`, `paths`, `shell`, and a Claude-specific `allowed-tools` syntax such as `Bash(git *) Read`.

Claude-only body syntax: `` !`cmd` `` dynamic shell injection, fenced `!` blocks, `$ARGUMENTS`, `$0`/`$1`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`.

Context behaviour: descriptions are always indexed, the full body loads on invoke and persists across turns, and auto-compaction retains the first 5,000 tokens per skill.

**Plugin packaging:** https://code.claude.com/docs/en/plugins-reference. Manifest at `.claude-plugin/plugin.json`, where only `name` is required and the manifest itself is optional when components sit in default locations. Everything else lives at the **plugin root, never inside `.claude-plugin/`**: `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `bin/`, `settings.json`. A single-skill plugin may put `SKILL.md` at the plugin root.

**Marketplace:** `.claude-plugin/marketplace.json` requiring `name`, `owner.name` and `plugins[]`, each entry needing `name` and `source`. Sources include a relative path, `github`, `git-subdir`, `npm`, `url`, `archive` and `command`.

**Evaluation:** `claude plugin eval` runs a suite of realistic prompts with graders of type `regex`, `tool_used`, `tool_order`, `file_exists`, `llm` and `baseline`. It runs two arms by default, with and without the plugin, and reports the delta. Each run starts in a throwaway home and config with only the plugin under test loaded. Requires Claude Code v2.1.269 or later.

---

## 4. One repo, two installers

**Shareable verbatim:** `SKILL.md` with `name`, `description`, `license`, `compatibility` and `metadata` frontmatter, the entire markdown body, and the `scripts/`, `references/`, `assets/` directories with their relative paths.

**Must be duplicated or adapted:**

| Concern | Claude Code | OpenAI |
|---|---|---|
| Install path | `.claude/skills/<n>/` | `.agents/skills/<n>/` |
| Plugin manifest | `.claude-plugin/plugin.json`, Claude schema | root `plugin.json`, agent-plugins.org 1.0.0 schema |
| Marketplace | `.claude-plugin/marketplace.json` | `.agents/plugins/marketplace.json` |
| UI metadata | `displayName` and `description` in plugin.json | `agents/openai.yaml` under `interface:` |
| Implicit invocation off | `disable-model-invocation: true` | `policy.allow_implicit_invocation: false` |

**Verified empirically:** Claude Code v2.1.278 does not natively discover `.agents/skills`. That path appears in the binary only inside the config importer, which copies such skills into `.claude/skills`. The string `agent-plugins.org` appears zero times in the binary while `.claude-plugin` appears 68 times, and the Claude Code docs never mention the portable manifest. The two layouts live at different paths, so one repository can carry both without conflict.

**Portability trap.** Claude Code's `` !`cmd` `` injection, `$ARGUMENTS` substitution and `Bash(git *)` tool syntax render as literal text in other clients. They must stay out of any SKILL.md intended to be shared.

---

## 5. Script execution

| Platform | Scripts run | Network | Package install | Timeout |
|---|---|---|---|---|
| Claude Code | Yes, via Bash as a normal user process | Full | Allowed; global installs discouraged | Not documented |
| Claude API skills | Yes, inside the code-execution container | **None.** Skills cannot make external calls | **None at runtime**, pre-installed packages only | Not documented |
| claude.ai | Yes, when code execution is enabled | Varies by user and admin settings | Not documented | Not documented |
| Codex CLI and IDE | Yes, in the OS sandbox | **Off by default** under `workspace-write`; opt in with `network_access = true` | Possible once network is on | Not documented |
| ChatGPT, non-Codex surfaces | Appears to be instructions-only, see uncertainties | n/a | n/a | n/a |

Codex sandbox modes are `read-only`, `workspace-write` (default) and `danger-full-access`, implemented with Seatbelt on macOS and bubblewrap on Linux (https://learn.chatgpt.com/docs/sandboxing).

Spec guidance for scripts (https://agentskills.io/skill-creation/using-scripts): make them self-contained with inline dependency declarations such as PEP 723 with `uv run`; **never prompt interactively**, because agents run non-interactive shells; write structured output to stdout and diagnostics to stderr; assume harnesses truncate beyond roughly 10,000 to 30,000 characters.

---

## 6. File input and output

| Platform | Accepts an uploaded file | Writes files out | Limits |
|---|---|---|---|
| Claude API | Yes, via Files API container blocks | Yes, returns a `file_id` | Max 20 skills per request; package under 30 MB uncompressed; description 1024 chars |
| claude.ai | Yes | Yes, when code execution runs | Skill zip must have the skill folder as its root, not nested. No published size cap found |
| Claude Code and Codex | Plain local filesystem | Yes, within the sandbox write scope | No documented size limit; Codex writes confined to the workspace |
| ChatGPT | Yes | Yes, in the data-analysis sandbox | Figures exist but could not be verified directly, see uncertainties |

---

## 7. Is a skill-only, no-MCP package useful?

**Yes, and OpenAI documents it explicitly** (https://developers.openai.com/plugins/concepts/skills):

> "A skill can also work without an MCP server when the workflow needs only packaged instructions and resources."

> "the MCP server provides data, authentication, authorization, and actions; the skill provides reusable instructions, examples, templates, and other resources."

On the Anthropic side, Claude Code skills require no MCP and the plugin manifest is itself optional. No Anthropic page was found that directly compares skills against MCP servers as a choice; every "skills vs MCP" comparison located was a vendor blog rather than documentation.

**The binding constraint is not MCP, it is the shell.** A skill-only package is fully useful wherever the agent has a filesystem and can execute: Claude Code, Codex CLI and IDE, Cursor, VS Code. It degrades where that is absent, and a product whose value depends on reaching a hosted service still needs MCP or network access.

---

## 8. What this forces on the toolkit design

Nine constraints follow directly from the above, before any product decision is made.

1. **Two installers, one source.** Ship `SKILL.md` plus `scripts/` once, and carry both `.claude-plugin/plugin.json` and a root `plugin.json` on the agent-plugins schema. They coexist at different paths. Anthropic has not adopted the portable manifest, so a single manifest is not an option.
2. **No Claude-only syntax in shared skill bodies.** No `` !`cmd` ``, no `$ARGUMENTS`, no `Bash(git *)`. If a Claude-specific convenience is worth having, it belongs in a separate Claude-only skill, not in the shared one.
3. **Scripts must be stdlib-only and offline.** Codex has network off by default and the Claude API container has no network and no runtime installs. Any deterministic script the toolkit ships must compute from a local file using the standard library alone. For the workflows under consideration, which are date arithmetic, percentile arithmetic and CSV classification, this costs nothing.
4. **Every script needs a no-script fallback.** Scripts are not auto-executed. In Claude Code, Bash requires permission and an administrator can disable skill shell execution entirely; on ChatGPT's chat surfaces execution appears unavailable. Each skill must therefore degrade to guided manual steps that reach the same output, more slowly.
5. **Scripts must never prompt.** All input arrives as arguments or as a file path. Structured output on stdout, diagnostics on stderr.
6. **SKILL.md stays under 500 lines and roughly 5,000 tokens.** Long checklists, field definitions and templates belong in `references/`, loaded on demand.
7. **The description is the product's discoverability surface.** It is capped at 1024 characters in the open spec, and OpenAI truncates descriptions first when the 8,000-character index budget is exceeded. It has to say what the skill does and when to use it, in that order, in plain words.
8. **Skill names are constrained and must match their directory.** Lowercase, hyphens, 64 characters, no double hyphens.
9. **There is a real evaluation path.** `claude plugin eval` with `tool_used`, `file_exists` and `llm` graders, run against a with-plugin and without-plugin arm, gives a measurable answer to "does this skill beat asking the model directly". That is the honest test for whether any of these workflows deserves to be a skill at all, and it should gate the MVP rather than follow it.

---

## 9. Uncertainties and what could not be verified

| Item | Status |
|---|---|
| Custom GPTs retire 11 December 2026 and Actions do not transfer automatically | **Uncertain.** The official Help Center article was identified but returns 403 to fetchers; dates come from a search-index summary. Re-verify in a browser before relying on it |
| ChatGPT skills are instructions-only on non-Codex surfaces | **Uncertain.** Inferred from documentation wording, never stated in those words. Material to constraint 4 |
| ChatGPT file limits: 512 MB per file, 2M tokens per document, about 50 MB for spreadsheets, 80 files per 3 hours | **Uncertain.** OpenAI Help Center is the source but the page is not directly fetchable |
| Agent Plugins 1.0.0 release date | **Uncertain.** Third-party blog only; the official site carries no date |
| Plan requirements for custom skills on claude.ai | **Conflicting.** Platform docs say Pro, Max, Team, Enterprise; the support article includes Free |
| Execution timeouts on any platform | **Not found** |
| Any published size limit for a skill package on OpenAI | **Not found** |
| claude.ai skill zip size limit or maximum skill count | **Not found** |
| Official Anthropic guidance choosing a skill over an MCP server | **Not found** |
| A formal statement that runtimes ignore unknown SKILL.md frontmatter keys | **Not found** in the skills spec. The agent-plugins spec does state it for `plugin.json` |

Nothing in section 8 depends on an item in this table except constraint 4, which is stated conservatively for that reason: the fallback is required regardless, because Claude Code alone can disable shell execution.
