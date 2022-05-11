# Jira Ticketing UI

The intention of this application is to provide non-technical users the ability to submit tickets to Jira in a controled enviornment. 
It requires that your Jira board contains an issue type named "Ticket" and a custom field that indicates the submitter's email address. 
Furthermore, you must access an API token from Atlasssian here:  https://id.atlassian.com/manage-profile/security/api-tokens 

# Usage

```
cd Jira_Tickets
docker build -t ticket_system . \
--build-arg jira_site={YOUR JIRA DOMAIN} \
--build-arg jira_project={YOUR JIRA PROJECT ABBR.} \
--build-arg jira_api={YOUR JIRA API} \
--build-arg jira_user={EMAIL FOR JIRA USER ISSUING API} \
--build-arg email_field={NUMBER FOR CUSTOM FIELD OF REQUESTER EMAIL ADDRESS} \
```

```
docker run -p 8129:8129 ticket_system
```