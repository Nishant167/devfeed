"""Junk-pattern filtering. See DEVFEED.md section 11 ("Junk patterns").

DEVFEED.md states the matching rule as: "the repository name is split on '-' and
'_', and each pattern is checked against whole tokens, so cloud-resources-manager
does not match resources and ml-course-recommender does not match course."

Read literally as "any whole token equals the pattern," those two examples would
actually match: "resources" IS one of the tokens of "cloud-resources-manager"
(tokens: cloud, resources, manager), and "course" IS one of the tokens of
"ml-course-recommender" (tokens: ml, course, recommender). For the stated examples
to come out negative, whole-token matching has to mean something more specific:
a pattern matches only against the **first or last** token(s) of the name, not an
arbitrary middle token. That reading makes both of DEVFEED.md's own examples come
out correctly (neither "resources" nor "course" sits at the start or end of its
example), and it also explains why some patterns carry an explicit '-' anchor:

- A leading '-' (e.g. "-awesome", "-questions", "-notes") anchors to the **last**
  token(s) only -- e.g. "awesome-repo-awesome" aside, "questions-forum" would NOT
  match "-questions" (that's a prefix), but "interview-questions" would.
- A trailing '-' (e.g. "awesome-", "interview-", "learning-", "study-",
  "practice-") anchors to the **first** token(s) only.
- A bare pattern with no dash anchor (e.g. "tutorial", "course", "resources",
  "my-portfolio", "100-days") matches at **either** the first or the last
  position, since it has no stated direction -- but never in the middle.

Multi-token patterns ("my-portfolio", "100-days") are themselves tokenized the
same way and matched as a contiguous run at the start or end of the name.

Worked check against DEVFEED.md's own examples:
- "cloud-resources-manager" -> tokens [cloud, resources, manager]. Pattern
  "resources" (bare) checks position 0 ([cloud]) and position -1 ([manager]) --
  neither is [resources], since it sits in the middle. No match. Matches
  DEVFEED.md's stated result (False).
- "ml-course-recommender" -> tokens [ml, course, recommender]. Pattern "course"
  (bare) checks [ml] and [recommender] -- "course" is the middle token. No match.
  Matches DEVFEED.md's stated result.
- "awesome-python" -> tokens [awesome, python]. Pattern "awesome-" is
  prefix-anchored, core token ["awesome"]; the first token is "awesome". Match ->
  True. Matches the acceptance criteria.
"""

from __future__ import annotations

from stage0.config import JUNK_PATTERNS


def _tokenize(name: str) -> list[str]:
    tokens: list[str] = []
    for part in name.lower().split("-"):
        tokens.extend(p for p in part.split("_") if p)
    return tokens


def _pattern_tokens(pattern: str) -> tuple[list[str], str]:
    """Returns (core_tokens, anchor), anchor in {'prefix', 'suffix', 'either'}."""
    p = pattern.lower()
    if p.startswith("-") and not p.endswith("-"):
        return _tokenize(p[1:]), "suffix"
    if p.endswith("-") and not p.startswith("-"):
        return _tokenize(p[:-1]), "prefix"
    return _tokenize(p), "either"


def is_junk(repo_name: str) -> bool:
    """True if repo_name's leading or trailing token(s) match a JUNK_PATTERNS
    entry (see module docstring for the whole-token / position semantics).
    Never a substring match within a single token."""
    repo_tokens = _tokenize(repo_name)
    if not repo_tokens:
        return False

    for pattern in JUNK_PATTERNS:
        core_tokens, anchor = _pattern_tokens(pattern)
        n = len(core_tokens)
        if n == 0 or n > len(repo_tokens):
            continue

        matches_prefix = repo_tokens[:n] == core_tokens
        matches_suffix = repo_tokens[-n:] == core_tokens

        if anchor == "prefix" and matches_prefix:
            return True
        if anchor == "suffix" and matches_suffix:
            return True
        if anchor == "either" and (matches_prefix or matches_suffix):
            return True

    return False
