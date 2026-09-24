# Documents: plain-English writing rules

Applies when the deliverable is a document: README, guide, report,
explainer, onboarding doc. The chat rules still hold, with these
adjustments for a standalone artifact.

## Gloss once

A document is standalone; readers may need the real term to search or
recognize it later. Give it once in parentheses on first mention ("a
login token (JWT)"), then use the plain word for the rest.

## One idea per sentence

Short sentences. If a sentence needs a semicolon or two commas to hold
together, split it.

## Structure earns its place

Headings and lists are fine. Plain does not mean flat. But no boilerplate:
no "Introduction", "Purpose of this document", "Conclusion", no "This
document will explain". Instructions address the reader directly: "Run
`npm install`", not "the user should run" or "it is recommended that".

## Exact artifacts verbatim

Same as chat: code, commands, file names, error strings stay exact. A
README nobody can copy-paste from has failed.

## Default shape

    # Title
    [one line: what this is; only if the title doesn't say it]
    ## [Section]
    ## [Section]

No abstract, no summary repeating the body, no "further reading" unless
asked. If another skill or template supplies the structure, these rules
govern the words inside it.

## Example

Bad:

> # todo-cli
> ## Introduction
> This document describes todo-cli, a task management utility that
> leverages a JSON-based persistence layer...

Good:

> # todo-cli
> A to-do list you use from the terminal. Tasks live in a `tasks.json`
> file next to the tool.
>
> ## Usage
> - `todo add 'buy milk'` adds a task
> - `todo list` shows all tasks
> - `todo done 2` marks task 2 done
