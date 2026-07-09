# Collaborative Troubleshooting Workflow

Use this workflow when:
- Simple fixes aren't working
- Issues are more complex than initially appeared
- Multiple attempts have failed
- The problem requires deeper investigation

## Investigation Phase

**Autonomous evidence gathering:**

1. Identify potential access barriers first:
   - Check what information might be needed (logs, databases, production environments, external services)
   - Determine what you can't access due to permissions or local environment limitations
   - Attempt to access borderline cases to confirm availability

2. Request inaccessible information in ONE batch:
   - List everything you cannot access or determine
   - Ask for all needed information at once
   - Be specific about what you need and why

3. Collect all accessible evidence while waiting:
   - Read error messages, stack traces, and logs you can access
   - Examine relevant code sections
   - Review configuration files
   - Check recent changes (git history, deployment logs)
   - Run diagnostic commands within your environment

**Example:**
"To investigate fully, I need: (1) the production logs from the last hour, (2) access to the database schema, and (3) clarification on whether service X is supposed to auto-restart. I'll continue examining the code in the meantime."

**Avoid:** Piecemeal requests that require multiple back-and-forth exchanges.

**Check in only when:**
- Genuinely blocked from proceeding
- Information is ambiguous enough to affect diagnosis
- Need domain knowledge you don't have

## Root Cause Analysis

**Analysis approach:**
1. Trace the causal chain backward from symptom to origin
2. Distinguish correlation from causation
3. Identify the earliest point of failure
4. Determine if this is a one-time issue or systemic problem

**Proceed autonomously when:**
- Root cause is clear from evidence
- Single plausible explanation
- Standard issue with known solutions

**Check in when:**
- Multiple plausible root causes exist
- Evidence points in different directions
- Requires domain/system knowledge you lack
- Systemic or architectural issues are uncovered

**Format for clear findings:**
"Root cause: [X]. This occurs because [explanation]. Evidence: [supporting data]."

**Format for ambiguous findings:**
"This could be either [A] or [B]. [A] would mean [X], while [B] would mean [Y]. Which matches your setup?"

## Solution Design & Implementation

**Implement autonomously when:**
- Proper fix is straightforward and addresses root cause
- No significant tradeoffs or side effects
- Solution is within normal scope and patterns

**Check in when:**
- Only bandaid/workaround solutions are available without more information
- Solution has significant tradeoffs (performance, complexity, maintainability)
- Architectural or design decisions are needed
- Multiple valid approaches exist with different implications

**Tradeoff presentation format:**
"I can fix this by [Option A] (pros/cons) or [Option B] (pros/cons). Which matters more for this use case?"

## Verification

**Autonomous verification:**
- Run existing tests
- Verify the specific symptom is resolved
- Check for obvious regressions
- Confirm the fix addresses the root cause, not just symptoms

**Check in only when:**
- Cannot verify without user's environment or data
- Need confirmation that the issue is fully resolved
- Verification reveals additional issues

## Key Principles

### Batch Information Requests
❌ "Can I see the config?" → *reviews* → "Now the logs?" → *reviews* → "Also the database?"
✅ "To diagnose this, I need: the config file, recent logs, and the database schema."

### Be Explicit About Limitations
- "I can't access [X] to verify this hypothesis"
- "I don't know if [architectural decision] is intentional, which affects the fix approach"
- "I need to understand [Y] before I can determine the root cause"

### Default to Action, Not Permission
For standard diagnostic activities, proceed autonomously. Only ask permission for:
- Potentially disruptive actions (modifying production, installing dependencies)
- When multiple valid approaches exist
- When you'd be implementing a bandaid without root cause understanding