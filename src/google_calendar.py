"""Google Calendar API client."""

import logging
import os
import pickle
from datetime import datetime
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarClient:
    """Client for accessing Google Calendar API."""
    
    def __init__(self, credentials_file: str = 'credentials.json', 
                 token_file: str = 'token.json', calendar_id: str = 'primary'):
        """Initialize the Google Calendar client.
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store/load access token
            calendar_id: Google Calendar ID to sync to
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.calendar_id = calendar_id
        self.service = None
        self.creds = None
        
    def authenticate(self) -> None:
        """Authenticate with Google Calendar API."""
        self.creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If credentials are not valid, refresh or re-authenticate
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info("Refreshing Google Calendar credentials")
                self.creds.refresh(Request())
            else:
                logger.info("Starting Google Calendar authentication flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Build the service
        self.service = build('calendar', 'v3', credentials=self.creds)
        logger.info("Successfully authenticated with Google Calendar")
    
    def create_event(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Create an event in Google Calendar.
        
        Args:
            event_data: Event data dictionary
            
        Returns:
            Google Calendar event ID if successful, None otherwise
        """
        if not self.service:
            self.authenticate()
        
        try:
            # Convert event data to Google Calendar format
            google_event = self._convert_to_google_format(event_data)
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=google_event
            ).execute()
            
            event_id = created_event.get('id')
            logger.info(f"Created event: {event_data.get('summary', 'No title')} (ID: {event_id})")
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to create event '{event_data.get('summary', 'No title')}': {e}")
            return None
    
    def update_event(self, google_event_id: str, event_data: Dict[str, Any]) -> bool:
        """Update an existing event in Google Calendar.
        
        Args:
            google_event_id: Google Calendar event ID
            event_data: Updated event data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            self.authenticate()
        
        try:
            # Convert event data to Google Calendar format
            google_event = self._convert_to_google_format(event_data)
            
            # Update the event
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=google_event_id,
                body=google_event
            ).execute()
            
            logger.info(f"Updated event: {event_data.get('summary', 'No title')} (ID: {google_event_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update event '{event_data.get('summary', 'No title')}': {e}")
            return False
    
    def get_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get events from Google Calendar within the specified date range.
        
        Args:
            start_date: Start date for event retrieval
            end_date: End date for event retrieval
            
        Returns:
            List of Google Calendar events
        """
        if not self.service:
            self.authenticate()
        
        try:
            # Convert datetime to RFC3339 format
            time_min = start_date.isoformat()
            time_max = end_date.isoformat()
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Found {len(events)} events in Google Calendar")
            return events
            
        except Exception as e:
            logger.error(f"Failed to fetch Google Calendar events: {e}")
            return []
    
    def _convert_to_google_format(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert event data to Google Calendar API format.
        
        Args:
            event_data: Event data from Yandex Calendar
            
        Returns:
            Google Calendar API formatted event
        """
        google_event = {
            'summary': event_data.get('summary', 'No Title'),
            'description': event_data.get('description', ''),
        }
        
        # Add location if present
        if event_data.get('location'):
            google_event['location'] = event_data['location']
        
        # Handle start and end times
        start_time = event_data['start_time']
        end_time = event_data['end_time']
        
        if event_data.get('is_all_day', False):
            # All-day event
            google_event['start'] = {
                'date': start_time.strftime('%Y-%m-%d'),
                'timeZone': 'UTC'
            }
            google_event['end'] = {
                'date': end_time.strftime('%Y-%m-%d'),
                'timeZone': 'UTC'
            }
        else:
            # Timed event
            google_event['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': str(start_time.tzinfo) if start_time.tzinfo else 'UTC'
            }
            google_event['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': str(end_time.tzinfo) if end_time.tzinfo else 'UTC'
            }
        
        # Add original Yandex UID as extended property for tracking
        google_event['extendedProperties'] = {
            'private': {
                'yandex_uid': event_data.get('uid', ''),
                'sync_source': 'yandex_calendar'
            }
        }
        
        return google_event