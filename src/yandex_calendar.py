"""Yandex Calendar CalDAV client."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import caldav
from caldav.elements import dav, cdav
import pytz

logger = logging.getLogger(__name__)


class YandexCalendarClient:
    """Client for accessing Yandex Calendar via CalDAV."""
    
    def __init__(self, username: str, password: str, caldav_url: str = "https://caldav.yandex.ru"):
        """Initialize the Yandex Calendar client.
        
        Args:
            username: Yandex username/email
            password: Yandex password or app password
            caldav_url: CalDAV server URL
        """
        self.username = username
        self.password = password
        self.caldav_url = caldav_url
        self.client = None
        self.principal = None
        self.calendar = None
        
    def connect(self) -> None:
        """Connect to Yandex CalDAV server."""
        try:
            logger.info(f"Connecting to Yandex CalDAV at {self.caldav_url}")
            self.client = caldav.DAVClient(
                url=self.caldav_url,
                username=self.username,
                password=self.password
            )
            
            self.principal = self.client.principal()
            calendars = self.principal.calendars()
            
            if not calendars:
                raise ValueError("No calendars found in Yandex account")
            
            # Use the first calendar found (usually the main calendar)
            self.calendar = calendars[0]
            logger.info(f"Connected to calendar: {self.calendar.name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Yandex Calendar: {e}")
            raise
    
    def get_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get events from Yandex Calendar within the specified date range.
        
        Args:
            start_date: Start date for event retrieval
            end_date: End date for event retrieval
            
        Returns:
            List of event dictionaries
        """
        if not self.calendar:
            self.connect()
        
        try:
            logger.info(f"Fetching events from {start_date} to {end_date}")
            
            # Search for events in the date range
            events = self.calendar.search(
                start=start_date,
                end=end_date,
                event=True,
                expand=True
            )
            
            parsed_events = []
            for event in events:
                try:
                    parsed_event = self._parse_event(event)
                    if parsed_event:
                        parsed_events.append(parsed_event)
                except Exception as e:
                    logger.warning(f"Failed to parse event: {e}")
                    continue
            
            logger.info(f"Found {len(parsed_events)} events")
            return parsed_events
            
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            raise
    
    def _parse_event(self, event) -> Dict[str, Any]:
        """Parse a CalDAV event into a standardized dictionary.
        
        Args:
            event: CalDAV event object
            
        Returns:
            Parsed event dictionary
        """
        try:
            # Get the iCal component
            component = event.icalendar_component
            
            # Extract basic event information
            summary = str(component.get('SUMMARY', ''))
            description = str(component.get('DESCRIPTION', ''))
            location = str(component.get('LOCATION', ''))
            uid = str(component.get('UID', ''))
            
            # Handle start and end times
            dtstart = component.get('DTSTART')
            dtend = component.get('DTEND')
            
            if dtstart:
                start_time = dtstart.dt
                if isinstance(start_time, datetime):
                    if start_time.tzinfo is None:
                        start_time = pytz.UTC.localize(start_time)
                else:
                    # All-day event
                    start_time = datetime.combine(start_time, datetime.min.time())
                    start_time = pytz.UTC.localize(start_time)
            else:
                return None
            
            if dtend:
                end_time = dtend.dt
                if isinstance(end_time, datetime):
                    if end_time.tzinfo is None:
                        end_time = pytz.UTC.localize(end_time)
                else:
                    # All-day event
                    end_time = datetime.combine(end_time, datetime.min.time())
                    end_time = pytz.UTC.localize(end_time)
            else:
                # Default to 1 hour duration
                end_time = start_time + timedelta(hours=1)
            
            # Check if it's an all-day event
            is_all_day = not isinstance(component.get('DTSTART').dt, datetime)
            
            return {
                'uid': uid,
                'summary': summary,
                'description': description,
                'location': location,
                'start_time': start_time,
                'end_time': end_time,
                'is_all_day': is_all_day,
                'raw_event': str(component)
            }
            
        except Exception as e:
            logger.error(f"Error parsing event: {e}")
            return None