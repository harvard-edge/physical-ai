# Web Development Server

The production interface is packaged under
`body/reachy_playground/static/` and served by the native robot app. This folder
provides a Mac development and simulation server for that same interface.

```sh
./code/web/run.sh
REACHY_FAKE=1 ./code/web/run.sh
```

Open `http://127.0.0.1:8080`. `/api/chat` uses the same Groq understanding and
memory classes as the native app. The only development-specific part is the
physical adapter. It either drives Reachy over the network or uses browser
speech in simulation.

`server.py` contains the FastAPI routes and development adapter. `run.sh` starts
the server and defaults the robot hostname to `reachy-mini.local`.
