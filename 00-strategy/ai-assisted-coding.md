# The AI-assisted coding round

Meta added this round in late 2025, and other companies are piloting similar formats. It isn't "let the
AI solve it". The interviewer watches how you **decompose, delegate, verify, and own** the code.

## Typical shape

- ~60 minutes, CoderPad-style editor with an AI chat panel. You can run code.
- A **progressive problem**: part 1 is easy, then requirements are added (e.g. key-value store → add TTL →
  add transactions → add persistence). Sometimes it starts from an existing codebase you must read and extend.
- The interviewer can see your prompts and which suggestions you accepted.

## What gets scored (common rubric themes)

| Area | Looks like |
|---|---|
| Problem solving | You state the approach and complexity **before** prompting. You pick the right data structures. |
| Code understanding & quality | You read every generated line, rename unclear names, remove dead code, keep functions small. |
| Verification | You write or ask for tests, check edge cases, and catch AI bugs (off-by-one, wrong complexity, mutated inputs). |
| Communication | You narrate. No long silences while the model generates. |

## A workflow that works

1. **Clarify** inputs, outputs, constraints, scale, and edge cases with the interviewer, not the AI.
2. **Design out loud:** data structures, API, complexity. Write a short plan as comments.
3. **Delegate small pieces:** "Implement `put(key, value, ttl)` using a dict plus a min-heap of expiries;
   O(log n) per put." Never "solve the problem".
4. **Review like a code reviewer:** read it, then explain it back in one sentence per block.
5. **Test:** ask the AI for edge-case tests, *then add your own*. Run them.
6. **Extend:** when the next requirement lands, revisit the design first, then prompt.

## Failure modes interviewers flag

- Pasting the whole prompt into the AI and accepting the output.
- Being unable to explain a line the AI wrote.
- Over-trusting complexity claims ("this is O(n)"... it's O(n²)).
- Never running the code, or running it without tests.
- Fighting the tool: re-prompting 5 times instead of fixing 2 lines by hand.

## Practice drill (30 min, twice a week)

Pick a medium "design a data structure" problem (LRU cache, rate limiter, in-memory KV store with TTL,
file system, leaderboard). Use any AI assistant with a timer:
- 5 min clarify + plan (out loud, recorded)
- 15 min build in delegated chunks
- 5 min tests and fixes
- 5 min extension (add one requirement)

Then review your recording: how often did you explain before prompting?

## Standard rounds still matter

Google's main coding environment is plain text with no execution, Meta's standard round has execution off,
and Amazon bans AI tools. **Keep doing unassisted practice** (see [../01-coding](../01-coding/README.md)).
