FROM python:3.9


# Set our working directory
WORKDIR /Ticketing_System

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN pip3 install -r requirements.txt


COPY . .

# Domain for Jira site
ENV JIRASITE = ${jira_site}
# Abbreviated code for Jira project
ENV JIRAPROJECT = ${jira_project}
# Jira API token. 
ENV JIRAAPI = ${jira_api}
# Jira User email issuing the api token. 
ENV JIRAUSER = ${jira_user}
# Number of the custom field containing the "requester's" email. 
ENV EMAILCUSTOMFIELD = ${email_field}



# main.py will run when container starts up on the device
CMD ["python3","-u","main.py"]
