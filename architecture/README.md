# MiOS architecture council

This directory contains the stable, inspectable design contracts for the MiOS
agent council. These are provider-neutral role definitions, not private model
prompts. The council collaborates through durable tasks, artifacts, and handoffs;
the coordinator is the only component allowed to advance controller state.

Roles are deliberately narrow. A worker may propose or produce an artifact, but
it cannot approve its own work, change policy, publish externally, or access the
robot. Those effects remain behind MiOS authority gates.
