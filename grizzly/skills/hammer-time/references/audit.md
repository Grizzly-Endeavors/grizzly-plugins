# Audit — Evaluating an Existing System

## Purpose

The hammer is pointed at something already built. A codebase, an infrastructure setup, a workflow, a process. It exists, it runs, and it's become fragile, overcomplicated, or hard to maintain. The user wants to know: what does this system actually need, and what can be cut?

## Workflow

### Step 1: Explore — Understand What *Is*

Before asking the user anything, assess the system yourself if you have the tools to do so. Look at the actual artifacts:

**If you have access to the codebase, infrastructure, configs, etc.:**
- Read the project structure. What components exist? How are they connected?
- Look at dependency files. What's pulled in? How heavy is the dependency tree?
- Check configuration files. How much config exists relative to actual logic?
- Look for dead code, unused imports, commented-out blocks, TODO markers.
- Check git history if available — what changes frequently? What hasn't been touched in months?
- Look at CI/CD pipelines, deployment configs, infrastructure definitions.
- Identify layers of abstraction. How many hops does a request or process take from start to finish?

**If you don't have access:**
Ask the user to describe the system. What are the components? What does the directory structure look like? What are the dependencies? What does the deployment process involve? Get as concrete a picture as possible of what actually exists.

The goal of this step is to build a factual inventory. No judgments yet — just understand what's there.

### Step 2: Clarify With the User

Now bring the user in to fill the gaps between what the system *is* and what it *does*:

- **What was it built for?** What was the original purpose or problem it was solving?
- **What does it actually do now?** Not what it *can* do — what do people actually use it for? Which paths get exercised? Which features have real users?
- **Where does it break?** What's fragile? What requires regular maintenance or firefighting? What are you afraid to touch?

The delta between these three answers is where the bloat lives. Something built for purpose A that now does purpose B with breakage at point C usually has a lot of leftover A infrastructure that B doesn't need, and C is often caused by the complexity of carrying both.

### Step 3: Drop the Hammer

Deliver the simplified vision following the output contract:

**Statement** → **Explanation** → **Handoff**

For each piece being identified as cuttable, connect back to the facts from Steps 1 and 2. "The event queue processes ~3 messages per day from a single source — a direct function call does the same thing" is the level of specificity to aim for.

Be concrete about what stays and why. The audit isn't just about cutting — it's about clarifying what the system's real skeleton is, so the user can see the shape of what they actually maintain.

## Important Caveats

**Acknowledge migration cost.** Unlike the other three workflows, auditing deals with something already running. Cutting a component has a cost — migration, testing, risk of regression. The hammer should account for this. Sometimes the hammer is "stop adding to this, and replace it next time you'd need to touch it" rather than "rip it out now."

**Watch for Chesterton's Fence.** If something exists and you can't immediately tell why, find out before recommending removal. It might be load-bearing in a way that isn't obvious. The goal is informed simplification, not blind deletion.

**Look for legacy compatibility weight.** Systems often carry significant complexity to maintain compatibility with another system, format, or workflow that hardly anyone still uses. A migration path that serves two active users might be dictating the architecture for the other two hundred. Identify these cases explicitly — sometimes dropping support for the legacy case and handling those users manually (or just communicating the change) removes an outsized amount of complexity.

## Example

**Context:** A user describes their CI/CD pipeline that has grown to include parallel test suites across three environments, a custom deployment orchestrator, canary deployments with automated rollback, feature flag integration, Slack notifications at every stage, artifact caching across multiple registries, and a custom dashboard for pipeline status.

**After exploration and clarification:** The pipeline deploys a low-traffic internal tool used by one team of eight people. Two incidents in the past year, both config errors. Feature flags manage two flags, one at 100% for six months. Dashboard tracks a pipeline that runs four times a day.

> **Run tests once, deploy straight to prod with a health check.** The pipeline is deploying an internal tool for eight people. Parallel environments made sense if deploys were high-risk, but both incidents this year were config errors that canary deploys wouldn't have caught. The custom orchestrator exists because the pipeline outgrew a simple config file, but it only outgrew it because of the multi-environment and canary complexity. The feature flags manage two flags — one fully rolled out for six months. The dashboard tracks four runs a day.
>
> A single test run, a direct deploy, and a health check endpoint that rolls back on failure covers what this team actually needs. The Slack notifications can stay — they're one line of config and genuinely useful. Everything else is infrastructure serving infrastructure.
>
> Anything there you'd push back on, or should we plan the teardown?
