"""CLI entry point: run IncidentIQ on a scenario and emit a post-mortem.

Usage:
    python -m incidentiq.main                 # local reasoning mode (offline)
    python -m incidentiq.main --foundry       # Microsoft Foundry agent (needs creds)
    python -m incidentiq.main --postmortem out.md
"""

from __future__ import annotations

import argparse

from . import agent, postmortem


def main() -> None:
    p = argparse.ArgumentParser(description="IncidentIQ root-cause reasoning agent")
    p.add_argument("--foundry", action="store_true", help="Run on Microsoft Foundry instead of local mode")
    p.add_argument("--postmortem", metavar="PATH", help="Write the post-mortem Markdown to PATH")
    p.add_argument("--quiet", action="store_true", help="Suppress the live reasoning print-out")
    args = p.parse_args()

    runner = agent.run_foundry if args.foundry else agent.run_local
    trace = runner(verbose=not args.quiet)

    if args.postmortem:
        with open(args.postmortem, "w", encoding="utf-8") as fh:
            fh.write(postmortem.to_markdown(trace))
        print(f"Post-mortem written to {args.postmortem}")


if __name__ == "__main__":
    main()
