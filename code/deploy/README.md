# Robot deployment bundle

The service file runs the wheel from `/opt/mayos-reachy/current`; releases are
stored in content-addressed-by-filename directories and the `current` symlink
is the only active pointer. `upgrade.sh` verifies a SHA-256 sidecar, performs a
health check, and restores the previous pointer on failure.

Installation and service activation are separate operator actions. The scripts
do not enable physical control, clear the persistent STOP state, or overwrite
robot data and credentials.
