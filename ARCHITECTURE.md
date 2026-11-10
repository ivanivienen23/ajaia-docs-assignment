# Architecture note

Python HTTP API, static responsive browser client and JSON persistence. The backend filters documents by current demo user and rejects viewer writes with 403. Presence is heartbeat plus polling, intentionally not realtime collaboration. Scope cuts favor zero-install reviewer setup.
