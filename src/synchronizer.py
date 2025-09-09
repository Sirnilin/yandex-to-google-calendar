"""Main synchronization logic for Yandex to Google Calendar sync."""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .yandex_calendar import YandexCalendarClient
from .google_calendar import GoogleCalendarClient
from .sync_state import SyncStateManager
from .config import Config

logger = logging.getLogger(__name__)


class CalendarSynchronizer:
    """Main class for synchronizing Yandex Calendar to Google Calendar."""
    
    def __init__(self):
        """Initialize the synchronizer with configured clients."""
        # Validate configuration
        Config.validate()
        
        # Initialize clients
        self.yandex_client = YandexCalendarClient(
            username=Config.YANDEX_USERNAME,
            password=Config.YANDEX_PASSWORD,
            caldav_url=Config.YANDEX_CALDAV_URL
        )
        
        self.google_client = GoogleCalendarClient(
            credentials_file=Config.GOOGLE_CREDENTIALS_FILE,
            token_file=Config.GOOGLE_TOKEN_FILE,
            calendar_id=Config.GOOGLE_CALENDAR_ID
        )
        
        self.state_manager = SyncStateManager(Config.STATE_FILE)
        
        # Statistics
        self.stats = {
            'total_yandex_events': 0,
            'new_events_synced': 0,
            'updated_events': 0,
            'errors': 0
        }
    
    def sync(self) -> Dict[str, Any]:
        """Perform a full synchronization.
        
        Returns:
            Dictionary with sync statistics
        """
        logger.info("Starting calendar synchronization")
        
        try:
            # Calculate date range for sync
            start_date = datetime.now() - timedelta(days=Config.DAYS_BEHIND)
            end_date = datetime.now() + timedelta(days=Config.DAYS_AHEAD)
            
            logger.info(f"Syncing events from {start_date.date()} to {end_date.date()}")
            
            # Fetch events from Yandex Calendar
            yandex_events = self.yandex_client.get_events(start_date, end_date)
            self.stats['total_yandex_events'] = len(yandex_events)
            
            if not yandex_events:
                logger.info("No events found in Yandex Calendar")
                return self.stats
            
            # Process each event
            current_yandex_uids = set()
            for event in yandex_events:
                yandex_uid = event.get('uid')
                if not yandex_uid:
                    logger.warning("Event without UID found, skipping")
                    continue
                
                current_yandex_uids.add(yandex_uid)
                
                try:
                    if self.state_manager.is_event_synced(yandex_uid):
                        # Event already synced, check if update is needed
                        google_event_id = self.state_manager.get_google_event_id(yandex_uid)
                        if self._update_event_if_needed(event, google_event_id):
                            self.stats['updated_events'] += 1
                    else:
                        # New event, sync it
                        if self._sync_new_event(event):
                            self.stats['new_events_synced'] += 1
                
                except Exception as e:
                    logger.error(f"Failed to process event '{event.get('summary', 'No title')}': {e}")
                    self.stats['errors'] += 1
            
            # Clean up tracking for deleted events
            self.state_manager.cleanup_old_events(current_yandex_uids)
            
            # Save state
            self.state_manager.save_state()
            
            logger.info(f"Sync completed: {self.stats['new_events_synced']} new, "
                       f"{self.stats['updated_events']} updated, "
                       f"{self.stats['errors']} errors")
            
            return self.stats
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            self.stats['errors'] += 1
            return self.stats
    
    def _sync_new_event(self, event: Dict[str, Any]) -> bool:
        """Sync a new event to Google Calendar.
        
        Args:
            event: Event data from Yandex Calendar
            
        Returns:
            True if successful, False otherwise
        """
        try:
            google_event_id = self.google_client.create_event(event)
            if google_event_id:
                self.state_manager.record_sync(event['uid'], google_event_id)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to sync new event: {e}")
            return False
    
    def _update_event_if_needed(self, event: Dict[str, Any], google_event_id: str) -> bool:
        """Update an event in Google Calendar if needed.
        
        Args:
            event: Event data from Yandex Calendar
            google_event_id: Google Calendar event ID
            
        Returns:
            True if event was updated, False otherwise
        """
        try:
            # For simplicity, we'll always update existing events
            # In a more sophisticated implementation, we could compare
            # event details to determine if an update is actually needed
            return self.google_client.update_event(google_event_id, event)
        except Exception as e:
            logger.error(f"Failed to update event: {e}")
            return False
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization statistics.
        
        Returns:
            Dictionary with sync statistics
        """
        return {
            'total_synced_events': self.state_manager.get_synced_count(),
            'last_sync': self.state_manager.get_last_sync_time(),
            'last_run_stats': self.stats
        }