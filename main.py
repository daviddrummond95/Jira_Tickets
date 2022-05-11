from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import jupyter_dash as dash
import pandas as pd
from dash.dependencies import Input, Output, State
import time

from jira import JIRA
import os

jira_site = os.environ.get('JIRASITE')
jira_project = os.environ.get('JIRAPROJECT')
api_token = os.environ.get('JIRAAPI')
jira_user = os.environ.get('JIRAUSER')
# number for custom field containing submitter info in jira
email_field = os.environ.get('EMAILCUSTOMFIELD')

# Some Authentication Methods
jira = JIRA(
    jira_site,
    basic_auth=(jira_user,api_token),  # Jira Cloud: a username/token tuple
)
 
#########################################################################################################
'''
USER INFO INPUTS ELEMENTS
'''
#########################################################################################################

first_name_input = html.Div(
    [
        dbc.Label("First Name"),
        dbc.Input(id="first-name-input", type="text", value=""),
    ]
)
last_name_input = html.Div(
    [
        dbc.Label("Last Name"),
        dbc.Input(id="last-name-input", type="text", value=""),
    ]
)
email_input = html.Div(
    [
        dbc.Label("Your Email"),
        dbc.Input(id="email-input", type="email", value=""),
    ]
)



#########################################################################################################
'''
BASIC REQUIREMENT ELEMENTS
'''
#########################################################################################################


# Ticket name element
subject = html.Div(
    [
        dbc.Label("Request Name"),
        dbc.Input(id="subject", type="text", placeholeder  = 'Please give your request a name.'),
    ]
)



# Define Reasons - This will determine priority on the backend
reasons=['Operational Excellence / Improvement', 'Operations Blocked', 'Apple Requested']

# Create reason dropdown element
dropdown = html.Div(
    [
        dbc.Label("Request Reason", html_for="purpose"),
        dcc.Dropdown(
            id="purpose",
            options=[{"label": i, "value": i} for i in reasons],
            
        )
    ],
    className="mb-3",
)




# Define the options for deliverable:
deliverables = ['New Report',
                'Report Modification',
                "Dashboard Modification",
                "Dashboard Fix",
                'New Dashboard']
# Create deliverable dropdown element
deliverable_type = html.Div(
    [
        dbc.Label("Deliverable", html_for="deliverable"),
        dcc.Dropdown(
            id="deliverable",
            options=[{"label": i, "value": i} for i in deliverables],
            
        )
    ],
    className="mb-3",
)

#########################################################################################################
'''
RECOMMENDED DESCRIPTION ELEMENTS
'''
#########################################################################################################

report_description = html.Div(
    [
        dbc.Label("Description", html_for="Description"),
        dbc.Textarea(
            id="Description",
            className="mb-3", placeholder="Please inlcude a detailed description of the request."
        ),
    ],
    className="mb-3",
)
question1 = html.Div(
    [
        dbc.Label("What problem do you want to solve with this request?", html_for="Question1"),
        dbc.Textarea(
            id="Question1",
            className="mb-3", placeholder="The response to this question is used to prioritize requests. The more detailed the response, the better we will be able to assess the business case for this problem"
        ),
    ],
    className="mb-3",
)

question2 = html.Div(
    [
        dbc.Label("What questions do you want answered with this request?", html_for="Question2"),
        dbc.Textarea(
            id="Question2",
            className="mb-3", placeholder="The more detail provided in this response, the better the assignee will be able to deliver on the need of the business."
        ),
    ],
    className="mb-3",
)

question3 = html.Div(
    [
        dbc.Label("What is your expectation for this request?", html_for="Question3"),
        dbc.Textarea(
            id="Question3",
            className="mb-3", placeholder="ie 'A Daily Email with X,Y,Z.' or 'We are looking to improve KPI X by Y% with a automation or model.'"
        ),
    ],
    className="mb-3",
)
button = dbc.Button("Submit", id='submit', className="me-2", n_clicks=0)

#########################################################################################################
'''
App Layout
'''
#########################################################################################################

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


# Define the form
initial_form = dbc.Card(html.Div([
                html.H1('New Request'),
                # User info card
                dbc.Card([html.Div([
                    html.H2('About You'),
                    dbc.Row([dbc.Col(first_name_input),dbc.Col(last_name_input),dbc.Col(email_input)])
                ], style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25})]),
                html.Br(),
                #Required basics card
                dbc.Card([html.Div([
                    html.H2('Required Basics'),
                    dbc.Row([ dbc.Col(dropdown), dbc.Col(deliverable_type)]),
                    subject,
                ], style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25})]),
                html.Br(),
                #Recommended Description card.
                dbc.Card([html.Div([
                    html.H2('Recommended Descriptions: '),
                    html.H3('Note we reserve the right to decline requests for failure to provide adequate detail.'),
                    report_description,
                    question1,
                    question2,
                    question3,
                    button,
                    html.Div(id='submission-status')
                ], style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25})]),
               ], style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25}), color="light")


app.layout = html.Div(
    html.Div([html.Div([
        dbc.Row(
            [
                dbc.Col(html.H1("Data Science Ticketing", style={'font-family': 'Arial Black', 'color' : '#ff3a00'}), width = {'size':'auto', 'offset':5}),   
            ],
        justify="around"
        ),
       ],style={'background-color':'black'},),
        html.Br(),
        html.Div(id="content", children = initial_form, style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25}),
        # Card for previously submitted tickets
        html.Div(dbc.Card(html.Div(id="content-2",
                          children = [html.H1('Your Tickets'), 
                                     # Define the table
                                      dash_table.DataTable(id = 'user-tickets',
                                                            # Conditional formating 
                                                           style_data_conditional=[
                                                                    {
                                                                        'if': {
                                                                            'filter_query': '{Status} contains "Done"',
                                                                        },
                                                                        'backgroundColor': 'green',
                                                                        'color': 'white'
                                                                    },
                                                                   {
                                                                        'if': {
                                                                            'filter_query': '{Status} contains "Rejected"',
                                                                        },
                                                                        'backgroundColor': '#8b0000',
                                                                        'color': 'white'
                                                                    },
                                                                ], 
                                                           style_data={
                                                                    'whiteSpace': 'normal',
                                                                    'height': 'auto',
                                                                   'backgroundColor': 'rgb(50, 50, 50)',
                                                                    'color': 'white',
                                                                   'font-family': 'Arial'
                                                                },
                                                           style_header={
                                                                'backgroundColor': 'rgb(30, 30, 30)',
                                                                'color': 'white',
                                                               'font-family': 'Arial Black'
                                                            },editable=True
                                                           )],
                          style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25})),style={'marginLeft': 25, 'marginRight': 25, 'marginTop':25, 'marginBottom':25} ),  
        dcc.Interval(id='refresh-once', interval=1,max_intervals=1),
        # Stores the data for future visits. 
        dcc.Store(id = 'first-name-store', storage_type='local'),
        dcc.Store(id = 'last-name-store', storage_type='local'),
        dcc.Store(id = 'email-store', storage_type='local'),
        html.Br()
    ]), style={'background-color':'#444', 'height': '300vh'})


#########################################################################################################
'''
App Functions
'''
#########################################################################################################

# Function to recall previously enterred email and name.
@app.callback(
    Output("email-input", "value"),
    Output("first-name-input", "value"),
    Output("last-name-input", "value"),
    Output('email-store','data'),
    Output('first-name-store', 'data'),
    Output('last-name-store', 'data'),
    Input("email-input", "value"),
    Input("first-name-input", "value"),
    Input("last-name-input", "value"),
    State('first-name-store', 'data'),
    State('last-name-store', 'data'),
    State('email-store','data'),
)
def get_subject(email_input, first_name_input, last_name_input, first_name_store, last_name_store, email_store):
    time.sleep(2)
    if email_input == '':
        email_input=email_store
    if first_name_input == '':
        first_name_input = first_name_store
    if last_name_input == '':
        last_name_input = last_name_store
    
    return email_input, first_name_input, last_name_input, email_input, first_name_input, last_name_input
            

# Creates the Jira ticket. 
@app.callback(
    Output('submission-status', 'children'),
    Input('submit', 'n_clicks'),
    State("subject", "value"),
    State("email-input", "value"),
    State("first-name-input", "value"),
    State("last-name-input", "value"),
    State("purpose", "value"),
    State("deliverable", "value"),
    State("Description", "value"),
    State("Question1", "value"),
    State("Question2", "value"),
    State("Question3", "value"),
    prevent_initial_call=True
)
def form_submission(n, request_name, email,first_name,last_name,purpose,deliverable,description= None, question1= None, question2=None, question3=None):
    if email is None:
             return dbc.Alert(
                    [
                        "Please include your email.",
                    ],
                    color="danger",
                )
    if not(first_name is not None and last_name is not None):
             return dbc.Alert(
                    [
                        "Please include your name.",
                    ],
                    color="danger",
                )
    if purpose is None:
        return dbc.Alert(
                    [
                        "Please include 'Request Reason'",
                    ],
                    color="danger",
                )
    if deliverable is None:
        return dbc.Alert(
                    [
                        "Please include the deliverable.",
                    ],
                    color="danger",
                )

    # What problem do you want to solve with this request?
    # What questions do you want answered with this request?
    # What is the success criteria for this request?
    description = '''h1. User Entry \n\nh2. Description\n\n {}\n\n
                    h2. Deliverable \n\n {}\n\n
                    h2. What problem do you want to solve with this request?\n\n {}\n\n
                    h2. What questions do you want answered with this request?\n\n {}\n\n
                    h2. What is the success criteria for this request?\n\n {}\n\n
                    h2. Submitter Info \n\n
                    Name: {} {} \n\n
                    Email: {}
                    '''.format(description, deliverable, question1, question2, question3, first_name,last_name, email)
    
    priority = "High" if purpose=='Operations Blocked' else "Medium"
    
    jira.create_issue(fields={
             'project': {'key': jira_project},
            'summary': request_name,
            'description': description,
            'issuetype': {'name': 'Ticket'},
             'customfield_{}'.format(email_field): email,
            'priority': {'name':priority},
            })
    
    
    return dbc.Alert(
                    [
                        "{} has been successfully requested. You will be updated with an expected timeframe in the next business day.".format(request_name),
                    ],
                    color="success",
                )

# Pulls all submitted tickets. 
@app.callback(
    Output('user-tickets','data'),Output('user-tickets','columns'),
    Input("email-input", "value")
)
def closed_errors(email):
    time.sleep(2)

    issues= jira.search_issues('cf[{}] ~ "{}"  order by created desc'.format(email_field, email))
    df = pd.DataFrame([[issue.fields.summary,  str(issue.fields.description).replace('                  ','').replace('\n\n',''' \n\n ''').replace(' \n \n ', ' \n\n ').replace('h1.', '###').replace('h2.','####'),issue.fields.status.name, pd.to_datetime(issue.fields.created).date()] for issue in issues], index = [issue.key for issue in issues],columns = ['Issue', 'Description', 'Status', 'Submission Date'])  
    return df.to_dict('records'), [{"name": i, "id": i, 'presentation': 'markdown',} for i in df.columns]
    
#########################################################################################################
'''
Run App
'''
#########################################################################################################

if __name__ == '__main__':

    app.run_server(host = '0.0.0.0', port = 8129, debug=True)

