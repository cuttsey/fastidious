# Security

Please report a vulnerability privately through GitHub's [private vulnerability reporting](../../security/advisories/new) rather than in a public issue.

## What to know before you run Fastidious

- **Keys.** `fastidious-motion` and the ElevenLabs skills read API keys from environment variables only. Nothing in this repository writes a key to a file, a prompt or a log. Keep keys out of project folders.
- **Third-party code.** `crew_stack.py` and `promo_stack.py` fetch skills from other people's repositories at pinned commits and refuse to install if the fetched commit differs. A pinned skill can still run its own scripts; read a package before moving its pin.
- **Uploads.** Image and video model APIs, and the optional `watch` skill's Gemini engine, send material to their providers. Do not send client, personal or confidential material without permission.
- **Browsers.** Several checks drive a headless Chrome against the page you give them. Point them only at pages you are entitled to test.
