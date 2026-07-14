"""Instant-feedback CLI: run a skill straight from the terminal, no MCP needed.

    python -m reachy_playground.play list
    python -m reachy_playground.play wiggle
    python -m reachy_playground.play ask_my_name Maya
    python -m reachy_playground.play say_text "Hello world"
    python -m reachy_playground.play nod 3

This is the fastest way to learn: edit a skill in skills.py, run it here, watch
the robot, repeat.
"""
import inspect
import sys

from . import skills


def _print_skills():
    print("Available skills:\n")
    for name, fn in skills.SKILLS.items():
        doc = (fn.__doc__ or "").strip().splitlines()[0] if fn.__doc__ else ""
        params = ", ".join(p.name for p in inspect.signature(fn).parameters.values())
        sig = f"({params})" if params else "()"
        print(f"  {name}{sig}\n      {doc}")
    print("\nRun one:  python -m reachy_playground.play <skill> [args...]")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("list", "-h", "--help"):
        _print_skills()
        return

    name, rest = args[0], args[1:]
    fn = skills.SKILLS.get(name)
    if fn is None:
        print(f"Unknown skill: {name!r}\n")
        _print_skills()
        sys.exit(1)

    # Map positional terminal args onto the skill's parameters, casting numbers.
    kwargs = {}
    for param, value in zip(inspect.signature(fn).parameters.values(), rest):
        if param.annotation is int:
            value = int(value)
        elif param.annotation is float:
            value = float(value)
        kwargs[param.name] = value

    print(f"Running {name}({kwargs})...")
    print(fn(**kwargs))


if __name__ == "__main__":
    main()
