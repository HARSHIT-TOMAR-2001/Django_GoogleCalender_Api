from django.shortcuts import render
from django.http import HttpResponseRedirect
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

# Google API credentials
CLIENT_SECRETS_FILE = './google_calender/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# Google Calendar Init View
def GoogleCalendarInitView(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return HttpResponseRedirect(authorization_url)

# Google Calendar Redirect View
def GoogleCalendarRedirectView(request):
    code = request.GET.get('code')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    service = build('calendar', 'v3', credentials=credentials)
    try:
        events = service.events().list(calendarId='primary', maxResults=10).execute()
        return render(request, 'calendar.html', {'events': events})
    except HttpError as error:
        return error
