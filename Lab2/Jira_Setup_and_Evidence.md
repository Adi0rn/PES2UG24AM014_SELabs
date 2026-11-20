# Jira setup and authentic evidence

The CSV provides the content for a Scrum backlog. These instructions are a reproduction plan; no Jira project or sprint is claimed to have been created.

1. In an available Jira Scrum project, enable the backlog, sprints and story-point estimation. Use synthetic donor and request data only.
2. Use the CSV importer available to your account. Map Issue Type, Summary, Description and Priority. Map Story Points to the project estimation field if it is offered. The Description repeats requirements, acceptance criteria and dependencies so these details survive import even without custom fields.
3. `Issue ID` contains local planning identifiers such as US-01. Keep these in a custom text field or prepend them to Summary. Do not map these strings to Jira's numeric import issue ID field without transforming them.
4. Import the four Epic rows first if the importer cannot resolve epic names in a single batch. Record the resulting Jira epic keys. For Story rows, map Epic Link to the appropriate epic key, or use the Parent field supported by your project. `Epic Name` and `Epic Link` are planning values, not pre-existing Jira keys. Do not assume Jira has linked the hierarchy automatically.
5. Create Sprint 1 and Sprint 2 in the backlog. Assign US-01 to US-05 to Sprint 1 and US-06 to US-10 to Sprint 2. Use existing sprint IDs if the importer requires them; otherwise assign through the backlog. Verify five stories and 24 points in each sprint and 48 points overall.
6. Set estimates before starting each sprint. Add the goals from README.md. Confirm dependencies and the Definition of Done in the report.
7. Capture the backlog with the Epic panel, priorities and story points. Start Sprint 1. Move stories through To Do, In Progress and Done as work is actually performed. Capture an active board; the included Day 3 simulation can be used as a rehearsal, not as proof of completed development.
8. Complete Sprint 1 only after its work satisfies the lab's simulation criteria. Capture Jira's completion result and burndown. Repeat for Sprint 2. Reports may require the sprint to have been started with estimates and completed through Jira's sprint controls.
9. Jira reports use actual transition timestamps. Clicking through an entire sprint in one session does not produce a historical five-day burndown. Do not backdate or present local chart values as Jira activity.
10. Save authentic captures in screenshots using the names below. Replace the report's local visual evidence section with or supplement it using those captures, and update the evidence status only after capture.

| Required file | Capture |
|---|---|
| screenshots/1_backlog_epics_story_points.png | 4 epics, 10 stories, priority and 48 points |
| screenshots/2_sprint1_active_board.png | Active Sprint 1 board with workflow columns |
| screenshots/3_sprint1_burndown.png | Jira Sprint 1 burndown report |
| screenshots/4_sprint2_burndown.png | Jira Sprint 2 burndown report |
| screenshots/sprint1_complete_dialog.png | Optional completion confirmation |

The files in simulation_visuals are explicitly labelled illustrations and must not be renamed or submitted as Jira screenshots.
