# Learning to use agents on Maziss

## What is running?

This conversation has a coordinating assistant. Native worker agents can be started
for specific assignments. The initial board demonstration uses an Art Director worker
and a Testing Director worker, each with a separate assignment and report file.

The product interface may show delegation tool activity, but this workspace does not
provide the coordinator with a separate user-visible agent-management screen. The
activity board is an offline HTML snapshot we control, not a claim that such a screen
exists. Ask “Which agents are running? Update the board” for a real tool-status check.
The coordinator can inspect agents, send instructions and interrupt its workers using
the available native tools. You direct those actions through this chat.

## Roles versus agents

A role is an instruction sheet: responsibility, context, allowed files and expected
output. An agent is an actual model worker carrying out an assignment. A file named
Art Director does not start a process. Different roles need not use different model
providers or subscriptions, and they do not automatically need subordinates.

Our role definitions are in agents/ROLES.md. AGENTS.md supplies shared project rules.
Those files preserve instructions for future work, but do not create a scheduler or
make agents work while no task is executing. Completed sessions can become unavailable;
the next task can start a new worker with the same role and saved project context.

## What you do

For the next increment, you can say:

“Run a small agent sprint to prepare the approved apartment art for the game. Show
assignments before work, use at most two workers at once, and have QA review the result.”

The coordinator writes bounded tasks, starts workers, records who actually ran, reviews
their outputs and updates the HTML board. You review the visual or playable result.
You can change direction, ask to stop a task, or request an explanation at any point.
You do not need to install an external agent framework for this initial workflow.

Useful requests:

- “Which agents are running now? Update the board.”
- “Explain this task brief before starting it.”
- “Have the Story Director review Maziss's dialogue for knowledge and motivation.”
- “Ask QA to challenge the proposed acceptance criteria.”
- “Stop the current workers and show what is complete.”
- “Keep this increment to one worker to limit my allowance.”

The board embeds worker reports and shows task IDs, objectives, file ownership,
acceptance criteria, actual worker names, status, results and timestamps in Paris time.
It is rebuilt by tools/build_agent_board.py from production/agent-board.json. It is
not connected directly to runtime status. Refreshing the page will not query agents.

## Method and next step

Use short increments: one meaningful goal, clear acceptance criteria, implementation,
independent review, then owner feedback. The coordinator combines CEO and liaison
responsibilities. Activate Art, Story, CTO, QA or Research only when the task needs
them. For a coding increment the CTO worker implements; QA checks separately.

Current priorities are in [BACKLOG.md](BACKLOG.md). The reference-based walking task
is paused and unapproved; the first Windows local run is the immediate owner check.
Before substantial work, show named assignments, allowed files, review criteria and
the worker limit. Future increments use feature branches and pull requests; the owner
controls creative acceptance and merge decisions. The initial checkpoint establishes
the existing project on main without marking unfinished art or motion as approved.

## Costs and limits

Native workers consume model usage and can exhaust the same allowance sooner. Parallel
workers do not create unlimited free capacity or guarantee better work. Keep tasks
small, avoid repeated full-context handoffs, and start with at most two workers.

No paid service, external AI API, new account or always-running agent server has been
set up. A genuinely independent background agent service would be a separate engineering
project involving hosting, credentials, permissions, execution controls and monitoring.
Do not add that infrastructure just to learn delegation inside this workspace.

## Project memory and GitHub

The approved visual starting point is art/proposals/apartment-cartoon-v2.png, recorded
in docs/ART_DIRECTION.md and AGENTS.md. This is durable project-file memory, not a
promise of permanent account-level ChatGPT memory. The initial source checkpoint saves
code, role files and task records to GitHub; future local edits still need commits and
pushes. GitHub Issues is the owner-visible backlog and pull requests are the change
review surface. Neither starts an agent automatically. There is no automatic live
agent/GitHub synchronization. The local HTML board remains a generated snapshot.
