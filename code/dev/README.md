# Development Adapters

This folder is not part of the installed robot package. It runs the same
website, Groq adapter, conversation policy, and memory logic on a Mac.

```sh
./code/dev/run.sh
REACHY_FAKE=1 ./code/dev/run.sh
```

`server.py` provides the development HTTP routes. `robot.py` contains the
network adapter and macOS speech path. Simulation uses browser speech when
Reachy is unavailable.
