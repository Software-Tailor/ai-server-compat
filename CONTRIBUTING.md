# Contributing

The most useful contribution is **evidence**: you ran a tool against AI Server and it worked, or it didn't.

- **Report a result:** open an issue with the tool and version, your AI Server version (`GET /api/version`),
  the model id, the configuration you used (no keys), and what happened.
- **Add a project:** edit `catalog/build_catalog.py` (not `projects.json` directly), then run
  `python build_catalog.py`. Only permissive licences (MIT, Apache-2.0, BSD); confirm the licence on GitHub
  and that the repo isn't archived. List the probe checks the tool *needs* (so a failing check blocks it)
  separately from those it can *use*.
- **Improve the probe:** each check must be independent, return pass / fail / skip with a one-line reason, and
  never crash the run.

No secrets in issues, code or results files. Contributions are accepted under the [MIT Licence](LICENSE).
