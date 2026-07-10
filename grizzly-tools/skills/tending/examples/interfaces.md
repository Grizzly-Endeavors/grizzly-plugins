# Interfaces — shapes cared-for *for the end user*

Concrete shapes that make a thing feel cared-for to whoever *uses* it, across whatever surface it presents — a web UI, a command-line tool, an API, a set of docs. This is the user's counterpart to `code.md`: the same instinct (imagine someone who isn't you, and who arrives without your context) pointed outward at the person on the other side of the interface.

The shapes are surface-agnostic. Each entry names the principle and then shows it landing across surfaces, because the *form* changes but the care does not — a good empty state in a UI and a good `--help` in a CLI are the same act.

Use this alongside `code.md` whenever what you are tending has a surface someone else operates. As recognition, the absence of these is a candidate. As target, these are what "usable" actually means.

---

## 1. Discoverability — the user can find it without already knowing it exists

The measure of a good interface is whether someone can succeed without being told the secret first. Make the paths findable from inside the thing.

- **CLI:** `--help` that actually lists what matters; `command --help` per subcommand; suggestions on a mistyped command ("did you mean…").
- **API:** a real reference, discoverable error responses that name the valid options, links or next-actions in payloads where it helps.
- **UI:** search, visible navigation, and empty states that teach the first action instead of showing a blank void.
- **Docs:** an index or table of contents, and search — so the answer is one hop away, not a full read-through.

## 2. Navigation that matches the user's mental model

Structure the surface the way the user already thinks about the problem, so they can *guess* where to go and be right. This is `code.md`'s "names you can guess," turned toward the person navigating.

Paths are predictable and shallow; related things sit together; the same concept has the same name in every corner of the surface. If a user has to build a private map of "where the thing I need is actually hidden," the navigation is doing the opposite of its job.

## 3. State that survives

Respect the effort the user has already spent. Losing their place, their input, or their selection tells them their work is cheap to you.

- **UI:** the back button works; a deep link returns them to where they were; a form that fails validation keeps what they typed; scroll and selection persist across a reasonable refresh.
- **CLI:** config and sensible session state persist so common invocations don't need re-specifying every time.
- **API:** idempotency where a retry is plausible, so a dropped connection doesn't cost the user their work or double it.
- **Everywhere:** never silently discard something the user took time to enter.

## 4. Help at the point of need

Put the explanation *where the question arises*, not buried in documentation the user would have to go find. The best help is the help you don't have to look for.

A tooltip or inline hint next to the confusing control; a label that says what the button will *do*, not just what it is; a CLI flag description that fits its one line; an API field doc that says the unit and the constraint. Reserve the manual for depth; answer the moment's question in the moment.

## 5. Feedback for every action

Nothing the user does should vanish into silence. The system should always say what is happening, what happened, and what it will do next.

- **UI:** loading and progress for anything slow; a clear success or failure state; confirmation that a saved thing saved.
- **CLI:** print what was done ("moved 12 files"), show progress on long work, and use a meaningful exit code so scripts can tell.
- **API:** honest status codes and a body that explains, not a bare 200-with-error-inside or an opaque 500.
- **Everywhere:** a slow operation with no signal is indistinguishable from a hung one — say something.

## 6. Errors that tell the user what to do next

The user-facing sibling of `code.md`'s "errors for the 3am debugger." An error the user sees should name what went wrong *and* the way forward, in their language — not a stack trace, not a bare code, not "something went wrong."

```
# less cared-for
Error 0x8007. Operation failed.

# more cared-for
Couldn't upload "report.pdf" — it's 42 MB and the limit is 25 MB.
Try compressing it, or split it into parts.
```

Where the system can recover or retry on the user's behalf, prefer that to making them figure it out.

## 7. Sensible defaults, with depth available

Make the common path easy and the rare path possible. The user shouldn't have to make a decision the system could reasonably make for them — but the choice should still be there when they want it. This is progressive disclosure aimed at the user.

Good default behavior with no flags; advanced options that exist without cluttering the first encounter; a docs quickstart that gets someone to a win before the reference material asks them to understand everything. The floor is low; the ceiling is high; the space between is uncluttered.

## 8. Forgiving of mistakes

People misread, mistype, and mis-click. A cared-for interface expects this and softens it rather than punishing it.

Accept reasonable variations of input; confirm or make reversible anything destructive (undo beats a scary dialog, and a scary dialog beats silent deletion); validate helpfully rather than rejecting flatly. The goal is that an honest mistake costs the user seconds, not their work.

## 9. Consistency across the whole surface

Learn it once, apply it everywhere. The same action should work the same way in every part of the interface, and the vocabulary should match across UI, CLI, API, and docs — so knowledge earned in one place transfers to the next.

Divergent terminology between the docs and the actual flags, or a delete that behaves differently in two screens, forces the user to relearn what they thought they knew. Consistency is a promise that their understanding will keep paying off.

## 10. Respecting time and attention

Fast where speed is felt; quiet where interruption isn't earned. Don't nag, don't block on things that could wait, and never trick the user into an action they didn't intend. A cared-for interface treats the user's attention as borrowed, not owned — no dark patterns, no manufactured urgency, no friction added to serve the product over the person.

---

## Care that adds

Each shape above can be present-but-rough — refine it — or missing outright — add it. The missing ones are what make a surface feel unloved even when nothing is *wrong*, and they are the findings surveys most often miss. Small, self-contained additions a user would feel immediately:

- a worked example in `--help` or at the top of the README quickstart
- an empty state that teaches the first action instead of showing a void
- a progress line for the operation that currently runs silent
- a "did you mean …" on the mistyped command or a link to the valid options in the error
- a confirmation (or better, an undo) on the destructive action that today just happens
- a meaningful exit code, so scripts can finally tell success from failure
