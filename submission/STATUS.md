# Submission and maintenance status

The author reported the **Build-stage submission as completed on 23 October 2026** in this project chat. This is a user-reported status; no portal receipt or judging decision has been independently verified.

- Submitted repository URL: https://github.com/rayanakarthikeyan/sevapath-esd
- Public working demo: https://rayanakarthikeyan.github.io/sevapath-esd/
- Repository baseline when submission was reported: `fa1ee40499c679a4864046861973327d3ae47c7a`
- Preserved baseline tag: [`build-stage-v1`](https://github.com/rayanakarthikeyan/sevapath-esd/tree/build-stage-v1)
- Current maintenance scope: reproducible installation, accurate documentation, evidence completeness, protected configuration and a working demo. The income-preparation workflow remains the submitted scope.
- Commit authorship and committer email: `rayanakarthikeyan@gmail.com`.

## Requirements boundary

The supplied three-page Build-stage PDF is mapped in [BUILD-CHECKLIST.md](BUILD-CHECKLIST.md). The application implements the relevant workflow, database, API, validation and authorization requirements; the pack includes source, setup, schema, sample data and actual test outcomes.

Two inputs remain unavailable: the earlier approved Design-stage artifact and the separate Final Demo guidelines PDF. Their requirements/conformance cannot be certified from the supplied materials. The screenshot lists the Demo stage on 25 October 2026; that date is not a substitute for its detailed guidelines.

## Maintenance checks

Every push/pull request runs the local behavior tests, production build and submission-artifact checks on Linux and Windows. The Pages deployment also refuses to publish if the database URL or public anonymous key is missing. The cloud CRUD suite is run explicitly using disposable synthetic records; it is not scheduled to write to the backend.

These automated checks cover the repository and build. They do not establish citizen impact, department approval, complete accessibility compliance or future availability of third-party hosting.
