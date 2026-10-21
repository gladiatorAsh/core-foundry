# Agents and tool use

## Workflow vs agent (lead with this distinction)

- **Workflow:** LLM calls orchestrated through **predefined code paths**: prompt chaining, routing,
  parallelization, orchestrator–workers, evaluator–optimizer. Predictable, testable, cheaper.
- **Agent:** the LLM **dynamically decides** its steps and tool calls in a loop until done. Use it for open-ended tasks
  where steps can't be predicted, and only with good tools, guardrails, and evals.
- Staff answer: "I'd start with a workflow and add agentic autonomy only where the task needs it."

## The agent loop

```
while not done and steps < MAX_STEPS and budget_left:
    response = llm(system_prompt, history, tool_schemas)
    if response.tool_calls:
        for call in response.tool_calls:
            validate args (schema) → check permission (user's identity) → maybe require approval
            result = execute(call) with timeout, idempotency key
            history.append(truncate(result))
    else:
        done = True
```

Patterns: **ReAct** (interleave reasoning and actions), **plan-and-execute** (plan first, then run steps,
re-plan on failure), **reflection** (critique and revise), **tree search** (rarely worth the cost in production).

## Tool design (most agent failures are tool failures)

- Few, well-named tools with clear descriptions, typed parameters (JSON schema), and examples of correct use.
- Return concise, structured results with actionable error messages ("customer_id not found; search by email instead").
- Make side-effecting tools **idempotent** (idempotency keys) and **reversible** where possible; separate read tools from write tools.
- Paginate and summarize large outputs; never dump 50K tokens into the context.
- **MCP (Model Context Protocol):** an open standard for exposing tools/resources/prompts to any compatible client, so tools are
  written once and reused across agents and apps. Mention it for platform-style designs.

## Multi-agent systems

- **Orchestrator–worker / supervisor:** a planner delegates subtasks to specialized agents (retrieval, coding, analysis) and merges results.
- **Pipeline:** fixed sequence of specialized agents (e.g. OCR → classify → extract → validate → human review).
- **Hand-offs:** a triage agent routes to domain agents (billing, tech support), passing a structured state.
- Benefits: specialization, parallelism, separate prompts/tools per role, smaller contexts.
- Costs: more tokens, coordination failures, harder debugging. Justify why one agent isn't enough.
- **Agent-to-agent protocols (e.g. A2A)** are emerging for cross-vendor agent interop; MCP is for agent ↔ tool.

## Memory

- **Short-term:** conversation history (summarize or window it to fit the budget).
- **Long-term:** user preferences/facts in a store, retrieved like RAG; write policies (what's worth saving), privacy controls, deletion.
- **Working state:** an explicit task state object (plan, completed steps, artifacts) is more reliable than relying on chat history.

## Reliability and safety for agents

- Step limits, token/cost budgets, wall-clock timeouts, loop detection (same call repeated).
- **Human-in-the-loop** approval for high-impact actions (payments, sending emails, deleting data).
- Least-privilege credentials; execute tools **as the user** (delegated auth), never with a god-mode service account.
- Treat all tool outputs and retrieved text as **untrusted** (indirect prompt injection); don't let them change instructions or permissions.
- Sandboxed code execution (containers/VMs with no network or allow-listed network).
- Full tracing of every step (inputs, tool calls, outputs, latency, cost) for debugging and audits.

## Evaluating agents

- **Task success rate** on scenario suites (with simulated users/tools), steps-to-success, cost and latency per task.
- Tool-call accuracy (right tool, valid args), recovery from tool errors, harmful-action rate (should be ~0).
- Trajectory review: sample traces weekly; turn failures into regression tests.
- Public benchmarks for reference: SWE-bench Verified (coding agents), τ-bench (tool use with simulated users), GAIA, WebArena.
