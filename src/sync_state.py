"""State management for tracking sync status."""

import json
import logging
from typing import Dict, Any, Set
from datetime import datetime

logger = logging.getLogger(__name__)


class SyncStateManager:
    """Manages synchronization state to avoid duplicates."""
    
    def __init__(self, state_file: str = 'sync_state.json'):
        """Initialize the sync state manager.
        
        Args:
            state_file: Path to the state file
        """
        self.state_file = state_file
        self.state = {
            'synced_events': {},  # yandex_uid -> google_event_id mapping
            'last_sync': None,
            'sync_count': 0
        }
        self.load_state()
    
    def load_state(self) -> None:
        """Load state from file."""
        try:
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
            logger.info(f"Loaded sync state with {len(self.state.get('synced_events', {}))} tracked events")
        except FileNotFoundError:
            logger.info("No existing state file found, starting fresh")
        except Exception as e:
            logger.warning(f"Failed to load state file: {e}, starting fresh")
    
    def save_state(self) -> None:
        """Save state to file."""
        try:
            self.state['last_sync'] = datetime.now().isoformat()
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.debug("Saved sync state")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
    
    def is_event_synced(self, yandex_uid: str) -> bool:
        """Check if an event has already been synced.
        
        Args:
            yandex_uid: Yandex Calendar event UID
            
        Returns:
            True if event is already synced
        """
        return yandex_uid in self.state.get('synced_events', {})
    
    def get_google_event_id(self, yandex_uid: str) -> str:
        """Get the Google Calendar event ID for a Yandex event.
        
        Args:
            yandex_uid: Yandex Calendar event UID
            
        Returns:
            Google Calendar event ID, or None if not found
        """
        return self.state.get('synced_events', {}).get(yandex_uid)
    
    def record_sync(self, yandex_uid: str, google_event_id: str) -> None:
        """Record that an event has been synced.
        
        Args:
            yandex_uid: Yandex Calendar event UID
            google_event_id: Google Calendar event ID
        """
        if 'synced_events' not in self.state:
            self.state['synced_events'] = {}
        
        self.state['synced_events'][yandex_uid] = google_event_id
        self.state['sync_count'] = self.state.get('sync_count', 0) + 1
        logger.debug(f"Recorded sync: {yandex_uid} -> {google_event_id}")
    
    def get_synced_count(self) -> int:
        """Get the number of synced events.
        
        Returns:
            Number of synced events
        """
        return len(self.state.get('synced_events', {}))
    
    def get_last_sync_time(self) -> str:
        """Get the last sync timestamp.
        
        Returns:
            ISO format timestamp string, or None if never synced
        """
        return self.state.get('last_sync')
    
    def cleanup_old_events(self, current_yandex_uids: Set[str]) -> None:
        """Remove tracking for events that no longer exist in Yandex Calendar.
        
        Args:
            current_yandex_uids: Set of current Yandex event UIDs
        """
        if 'synced_events' not in self.state:
            return
        
        synced_events = self.state['synced_events']
        old_uids = set(synced_events.keys()) - current_yandex_uids
        
        for uid in old_uids:
            del synced_events[uid]
            logger.debug(f"Removed tracking for deleted event: {uid}")
        
        if old_uids:
            logger.info(f"Cleaned up {len(old_uids)} old event mappings")