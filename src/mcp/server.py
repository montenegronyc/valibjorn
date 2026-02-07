"""ValiBjorn MCP Server — local SQLite persistence for validation runs."""

import asyncio
import json
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from src.db.database import execute_query, execute_one, execute_insert

server = Server("valibjorn")

# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

TOOLS = [
    Tool(
        name="valibjorn_create_concept",
        description="Create a new business concept to validate. Returns the concept_id.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Short name for the business concept",
                },
                "description": {
                    "type": "string",
                    "description": "1-3 sentence description of the idea",
                },
                "founder_context": {
                    "type": "string",
                    "description": "Full founder context (problem, customer, background, stage, constraints, goals, inferred fields)",
                },
                "business_type": {
                    "type": "string",
                    "description": "E.g. B2B SaaS, Marketplace, Dev Tools, etc.",
                },
            },
            "required": ["name", "founder_context"],
        },
    ),
    Tool(
        name="valibjorn_start_run",
        description="Start a new validation run for a concept. Returns the run_id. Call this before dispatching agents.",
        inputSchema={
            "type": "object",
            "properties": {
                "concept_id": {
                    "type": "integer",
                    "description": "The concept to validate",
                },
            },
            "required": ["concept_id"],
        },
    ),
    Tool(
        name="valibjorn_write_agent_output",
        description="Write a single agent's analysis output to the database. Called by each agent after completing its analysis.",
        inputSchema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "integer",
                    "description": "The validation run ID",
                },
                "agent_name": {
                    "type": "string",
                    "description": "Agent name: idea-validation, business-model, fundraising, go-to-market, product, sales, marketing-brand, growth-analytics, operations, finance-accounting, customer-success, legal-compliance",
                },
                "output": {
                    "type": "string",
                    "description": "The agent's full analysis text",
                },
                "confidence_score": {
                    "type": "number",
                    "description": "Agent's confidence score 0-100",
                },
                "signals": {
                    "type": "string",
                    "description": "JSON array of signals for other agents",
                },
                "risks": {
                    "type": "string",
                    "description": "JSON array of identified risks",
                },
                "frameworks_applied": {
                    "type": "string",
                    "description": "Comma-separated list of frameworks used",
                },
            },
            "required": ["run_id", "agent_name", "output"],
        },
    ),
    Tool(
        name="valibjorn_get_run_outputs",
        description="Get all agent outputs for a validation run. Use this in the Weave phase to read agent results without bloating context — returns summaries by default.",
        inputSchema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "integer",
                    "description": "The validation run ID",
                },
                "full": {
                    "type": "boolean",
                    "description": "If true, return full output text. If false (default), return summary with confidence, signals, and risks only.",
                },
            },
            "required": ["run_id"],
        },
    ),
    Tool(
        name="valibjorn_get_agent_output",
        description="Get a single agent's full output for a run. Use when you need the complete analysis from one specific agent.",
        inputSchema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "integer",
                    "description": "The validation run ID",
                },
                "agent_name": {
                    "type": "string",
                    "description": "The agent name to retrieve",
                },
            },
            "required": ["run_id", "agent_name"],
        },
    ),
    Tool(
        name="valibjorn_complete_run",
        description="Mark a validation run as complete and store the final brief, verdict, and scores.",
        inputSchema={
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "integer",
                    "description": "The validation run ID",
                },
                "verdict": {
                    "type": "string",
                    "description": "GO, PIVOT, or KILL",
                },
                "confidence_score": {
                    "type": "number",
                    "description": "Overall weighted confidence 0-100",
                },
                "overall_score": {
                    "type": "number",
                    "description": "Overall score out of 120",
                },
                "brief": {
                    "type": "string",
                    "description": "The complete Founder Operating Brief markdown",
                },
            },
            "required": ["run_id", "verdict"],
        },
    ),
    Tool(
        name="valibjorn_list_concepts",
        description="List all validated business concepts. Shows name, type, latest verdict, and run count.",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 20)",
                },
            },
        },
    ),
    Tool(
        name="valibjorn_get_concept",
        description="Get full details for a concept including its founder context and all validation runs.",
        inputSchema={
            "type": "object",
            "properties": {
                "concept_id": {
                    "type": "integer",
                    "description": "The concept ID",
                },
            },
            "required": ["concept_id"],
        },
    ),
    Tool(
        name="valibjorn_search",
        description="Search across concepts and agent outputs by keyword. Useful for finding past analyses on similar ideas, markets, or frameworks.",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term",
                },
                "scope": {
                    "type": "string",
                    "description": "Where to search: 'concepts', 'outputs', or 'all' (default)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 20)",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="valibjorn_compare_runs",
        description="Compare two validation runs side by side. Shows verdict, scores, and per-agent confidence differences.",
        inputSchema={
            "type": "object",
            "properties": {
                "run_id_a": {
                    "type": "integer",
                    "description": "First run ID",
                },
                "run_id_b": {
                    "type": "integer",
                    "description": "Second run ID",
                },
            },
            "required": ["run_id_a", "run_id_b"],
        },
    ),
    Tool(
        name="valibjorn_stats",
        description="Database statistics: concept count, run count, verdict distribution, agent output counts.",
        inputSchema={"type": "object", "properties": {}},
    ),
]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


def _handle_create_concept(args: dict) -> str:
    concept_id = execute_insert(
        "INSERT INTO concepts (name, description, founder_context, business_type) VALUES (?, ?, ?, ?)",
        (
            args["name"],
            args.get("description", ""),
            args["founder_context"],
            args.get("business_type", ""),
        ),
    )
    return f"Created concept #{concept_id}: {args['name']}"


def _handle_start_run(args: dict) -> str:
    concept = execute_one("SELECT id, name FROM concepts WHERE id = ?", (args["concept_id"],))
    if not concept:
        return f"Error: concept #{args['concept_id']} not found"
    run_id = execute_insert(
        "INSERT INTO validation_runs (concept_id) VALUES (?)",
        (args["concept_id"],),
    )
    return f"Started validation run #{run_id} for concept '{concept['name']}'"


def _handle_write_agent_output(args: dict) -> str:
    run = execute_one("SELECT id FROM validation_runs WHERE id = ?", (args["run_id"],))
    if not run:
        return f"Error: run #{args['run_id']} not found"

    output_id = execute_insert(
        """INSERT INTO agent_outputs
           (run_id, agent_name, output, confidence_score, signals, risks, frameworks_applied)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            args["run_id"],
            args["agent_name"],
            args["output"],
            args.get("confidence_score"),
            args.get("signals"),
            args.get("risks"),
            args.get("frameworks_applied"),
        ),
    )
    score_str = f" (confidence: {args['confidence_score']})" if args.get("confidence_score") else ""
    return f"Saved {args['agent_name']} output #{output_id} for run #{args['run_id']}{score_str}"


def _handle_get_run_outputs(args: dict) -> str:
    run_id = args["run_id"]
    full = args.get("full", False)

    run = execute_one(
        """SELECT r.id, r.status, r.verdict, r.confidence_score, r.overall_score,
                  c.name as concept_name
           FROM validation_runs r JOIN concepts c ON r.concept_id = c.id
           WHERE r.id = ?""",
        (run_id,),
    )
    if not run:
        return f"Error: run #{run_id} not found"

    outputs = execute_query(
        "SELECT * FROM agent_outputs WHERE run_id = ? ORDER BY agent_name",
        (run_id,),
    )

    lines = [
        f"## Run #{run_id} — {run['concept_name']}",
        f"Status: {run['status']} | Verdict: {run['verdict'] or 'pending'} | Confidence: {run['confidence_score'] or 'pending'}",
        f"Agents completed: {len(outputs)}/12",
        "",
    ]

    for o in outputs:
        lines.append(f"### {o['agent_name']}")
        lines.append(f"Confidence: {o['confidence_score'] or 'N/A'}")
        if o["signals"]:
            lines.append(f"Signals: {o['signals']}")
        if o["risks"]:
            lines.append(f"Risks: {o['risks']}")
        if o["frameworks_applied"]:
            lines.append(f"Frameworks: {o['frameworks_applied']}")
        if full:
            lines.append("")
            lines.append(o["output"])
        lines.append("")

    return "\n".join(lines)


def _handle_get_agent_output(args: dict) -> str:
    output = execute_one(
        "SELECT * FROM agent_outputs WHERE run_id = ? AND agent_name = ?",
        (args["run_id"], args["agent_name"]),
    )
    if not output:
        return f"No output found for agent '{args['agent_name']}' in run #{args['run_id']}"

    lines = [
        f"## {output['agent_name']} — Run #{args['run_id']}",
        f"Confidence: {output['confidence_score'] or 'N/A'}",
        f"Frameworks: {output['frameworks_applied'] or 'N/A'}",
        f"Signals: {output['signals'] or 'none'}",
        f"Risks: {output['risks'] or 'none'}",
        "",
        output["output"],
    ]
    return "\n".join(lines)


def _handle_complete_run(args: dict) -> str:
    run = execute_one("SELECT id FROM validation_runs WHERE id = ?", (args["run_id"],))
    if not run:
        return f"Error: run #{args['run_id']} not found"

    execute_query(
        """UPDATE validation_runs
           SET verdict = ?, confidence_score = ?, overall_score = ?,
               brief = ?, status = 'completed', completed_at = datetime('now')
           WHERE id = ?""",
        (
            args["verdict"],
            args.get("confidence_score"),
            args.get("overall_score"),
            args.get("brief"),
            args["run_id"],
        ),
    )
    return f"Run #{args['run_id']} completed: {args['verdict']}"


def _handle_list_concepts(args: dict) -> str:
    limit = min(max(1, args.get("limit", 20)), 100)
    rows = execute_query(
        """SELECT c.id, c.name, c.business_type, c.created_at,
                  COUNT(r.id) as run_count,
                  (SELECT verdict FROM validation_runs
                   WHERE concept_id = c.id ORDER BY created_at DESC LIMIT 1) as latest_verdict,
                  (SELECT confidence_score FROM validation_runs
                   WHERE concept_id = c.id ORDER BY created_at DESC LIMIT 1) as latest_confidence
           FROM concepts c LEFT JOIN validation_runs r ON c.id = r.concept_id
           GROUP BY c.id ORDER BY c.created_at DESC LIMIT ?""",
        (limit,),
    )
    if not rows:
        return "No concepts yet."

    lines = ["## ValiBjorn Concepts", ""]
    for r in rows:
        verdict = r["latest_verdict"] or "no runs"
        conf = f" ({r['latest_confidence']}%)" if r["latest_confidence"] else ""
        btype = f" [{r['business_type']}]" if r["business_type"] else ""
        lines.append(
            f"- **#{r['id']} {r['name']}**{btype} — {verdict}{conf} ({r['run_count']} runs) — {r['created_at']}"
        )
    return "\n".join(lines)


def _handle_get_concept(args: dict) -> str:
    concept = execute_one("SELECT * FROM concepts WHERE id = ?", (args["concept_id"],))
    if not concept:
        return f"Error: concept #{args['concept_id']} not found"

    runs = execute_query(
        """SELECT id, verdict, confidence_score, overall_score, status, created_at, completed_at
           FROM validation_runs WHERE concept_id = ? ORDER BY created_at DESC""",
        (args["concept_id"],),
    )

    lines = [
        f"## Concept #{concept['id']}: {concept['name']}",
        f"Type: {concept['business_type'] or 'unspecified'}",
        f"Created: {concept['created_at']}",
        "",
        "### Founder Context",
        concept["founder_context"] or "(none)",
        "",
        f"### Validation Runs ({len(runs)})",
    ]

    for r in runs:
        agent_count = execute_one(
            "SELECT COUNT(*) as cnt FROM agent_outputs WHERE run_id = ?", (r["id"],)
        )
        cnt = agent_count["cnt"] if agent_count else 0
        lines.append(
            f"- Run #{r['id']}: {r['verdict'] or 'pending'} "
            f"(confidence: {r['confidence_score'] or '?'}, score: {r['overall_score'] or '?'}/120) "
            f"— {r['status']} — {cnt} agents — {r['created_at']}"
        )

    return "\n".join(lines)


def _handle_search(args: dict) -> str:
    query = args["query"]
    scope = args.get("scope", "all")
    limit = min(max(1, args.get("limit", 20)), 100)
    pattern = f"%{query}%"
    lines = [f"## Search: '{query}' (scope: {scope})", ""]

    if scope in ("concepts", "all"):
        rows = execute_query(
            """SELECT id, name, business_type, description
               FROM concepts
               WHERE name LIKE ? OR description LIKE ? OR founder_context LIKE ? OR business_type LIKE ?
               LIMIT ?""",
            (pattern, pattern, pattern, pattern, limit),
        )
        lines.append(f"### Concepts ({len(rows)} matches)")
        for r in rows:
            lines.append(f"- #{r['id']} **{r['name']}** [{r['business_type'] or '?'}] — {(r['description'] or '')[:100]}")
        lines.append("")

    if scope in ("outputs", "all"):
        rows = execute_query(
            """SELECT ao.id, ao.agent_name, ao.run_id, ao.confidence_score,
                      ao.frameworks_applied, c.name as concept_name,
                      SUBSTR(ao.output, 1, 200) as excerpt
               FROM agent_outputs ao
               JOIN validation_runs r ON ao.run_id = r.id
               JOIN concepts c ON r.concept_id = c.id
               WHERE ao.output LIKE ? OR ao.signals LIKE ? OR ao.risks LIKE ?
               LIMIT ?""",
            (pattern, pattern, pattern, limit),
        )
        lines.append(f"### Agent Outputs ({len(rows)} matches)")
        for r in rows:
            lines.append(
                f"- **{r['agent_name']}** (run #{r['run_id']}, {r['concept_name']}) "
                f"confidence: {r['confidence_score'] or '?'} — {r['excerpt']}..."
            )
        lines.append("")

    return "\n".join(lines)


def _handle_compare_runs(args: dict) -> str:
    run_a = execute_one(
        """SELECT r.*, c.name as concept_name
           FROM validation_runs r JOIN concepts c ON r.concept_id = c.id
           WHERE r.id = ?""",
        (args["run_id_a"],),
    )
    run_b = execute_one(
        """SELECT r.*, c.name as concept_name
           FROM validation_runs r JOIN concepts c ON r.concept_id = c.id
           WHERE r.id = ?""",
        (args["run_id_b"],),
    )
    if not run_a or not run_b:
        return "Error: one or both runs not found"

    outputs_a = {
        r["agent_name"]: r
        for r in execute_query(
            "SELECT agent_name, confidence_score, risks, signals FROM agent_outputs WHERE run_id = ?",
            (args["run_id_a"],),
        )
    }
    outputs_b = {
        r["agent_name"]: r
        for r in execute_query(
            "SELECT agent_name, confidence_score, risks, signals FROM agent_outputs WHERE run_id = ?",
            (args["run_id_b"],),
        )
    }

    lines = [
        "## Run Comparison",
        "",
        f"| | Run #{args['run_id_a']} ({run_a['concept_name']}) | Run #{args['run_id_b']} ({run_b['concept_name']}) |",
        "|---|---|---|",
        f"| Verdict | {run_a['verdict'] or '?'} | {run_b['verdict'] or '?'} |",
        f"| Confidence | {run_a['confidence_score'] or '?'} | {run_b['confidence_score'] or '?'} |",
        f"| Score | {run_a['overall_score'] or '?'}/120 | {run_b['overall_score'] or '?'}/120 |",
        "",
        "### Per-Agent Confidence",
        "",
        "| Agent | Run A | Run B | Delta |",
        "|---|---|---|---|",
    ]

    all_agents = sorted(set(list(outputs_a.keys()) + list(outputs_b.keys())))
    for agent in all_agents:
        a_score = outputs_a.get(agent, {}).get("confidence_score")
        b_score = outputs_b.get(agent, {}).get("confidence_score")
        a_str = str(a_score) if a_score is not None else "—"
        b_str = str(b_score) if b_score is not None else "—"
        if a_score is not None and b_score is not None:
            delta = b_score - a_score
            delta_str = f"{delta:+.0f}"
        else:
            delta_str = "—"
        lines.append(f"| {agent} | {a_str} | {b_str} | {delta_str} |")

    return "\n".join(lines)


def _handle_stats(args: dict) -> str:
    concepts = execute_one("SELECT COUNT(*) as cnt FROM concepts")
    runs = execute_one("SELECT COUNT(*) as cnt FROM validation_runs")
    outputs = execute_one("SELECT COUNT(*) as cnt FROM agent_outputs")
    verdicts = execute_query(
        "SELECT verdict, COUNT(*) as cnt FROM validation_runs WHERE verdict IS NOT NULL GROUP BY verdict"
    )
    agents = execute_query(
        "SELECT agent_name, COUNT(*) as cnt, AVG(confidence_score) as avg_conf FROM agent_outputs GROUP BY agent_name ORDER BY agent_name"
    )

    lines = [
        "## ValiBjorn Stats",
        "",
        f"- Concepts: {concepts['cnt']}",
        f"- Validation runs: {runs['cnt']}",
        f"- Agent outputs: {outputs['cnt']}",
        "",
        "### Verdict Distribution",
    ]
    for v in verdicts:
        lines.append(f"- {v['verdict']}: {v['cnt']}")

    if agents:
        lines.append("")
        lines.append("### Agent Averages")
        lines.append("| Agent | Outputs | Avg Confidence |")
        lines.append("|---|---|---|")
        for a in agents:
            avg = f"{a['avg_conf']:.0f}" if a["avg_conf"] else "—"
            lines.append(f"| {a['agent_name']} | {a['cnt']} | {avg} |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

_TOOL_HANDLERS = {
    "valibjorn_create_concept": _handle_create_concept,
    "valibjorn_start_run": _handle_start_run,
    "valibjorn_write_agent_output": _handle_write_agent_output,
    "valibjorn_get_run_outputs": _handle_get_run_outputs,
    "valibjorn_get_agent_output": _handle_get_agent_output,
    "valibjorn_complete_run": _handle_complete_run,
    "valibjorn_list_concepts": _handle_list_concepts,
    "valibjorn_get_concept": _handle_get_concept,
    "valibjorn_search": _handle_search,
    "valibjorn_compare_runs": _handle_compare_runs,
    "valibjorn_stats": _handle_stats,
}


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    handler = _TOOL_HANDLERS.get(name)
    if not handler:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    try:
        result = handler(arguments)
    except Exception as e:
        result = f"Error: {e}"
    return [TextContent(type="text", text=result)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
