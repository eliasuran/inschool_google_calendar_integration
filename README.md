integration between visma inschool and google calendar. *visma inschool* -> *google calendar*

### Requirements:
- google developer user / project
- Feide user with access to Visma InSchool

### Stack:
- python (lul)

not using visma inschool API because can't find one and cba since it's unlikely to get access anyway if it exists


### How it works

- Logging in to Visma InSchool through Feide
- Getting InSchool authorization JWT
- Doing Google OAuth process to get access to Google Calendar
- Using JWT as bearer auth token to fetch timetable from InSchool API
- Creating a calendar specifically for timetable (*Timeplan*), storing ID locally (should likely be improved, unless it auto deletes on name conflict)
- Deleting existing events for weeks in scope
- Creating events for weeks in scope
