#!/usr/bin/env python3
"""Test script to validate the application structure and functionality."""

import sys
import os
import tempfile
import json
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from config import Config
        print("✅ Config import successful")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from yandex_calendar import YandexCalendarClient
        print("✅ YandexCalendarClient import successful")
    except Exception as e:
        print(f"❌ YandexCalendarClient import failed: {e}")
        return False
    
    try:
        from google_calendar import GoogleCalendarClient
        print("✅ GoogleCalendarClient import successful")
    except Exception as e:
        print(f"❌ GoogleCalendarClient import failed: {e}")
        return False
    
    try:
        from sync_state import SyncStateManager
        print("✅ SyncStateManager import successful")
    except Exception as e:
        print(f"❌ SyncStateManager import failed: {e}")
        return False
    
    try:
        from synchronizer import CalendarSynchronizer
        print("✅ CalendarSynchronizer import successful")
    except Exception as e:
        print(f"❌ CalendarSynchronizer import failed: {e}")
        return False
    
    return True


def test_sync_state_manager():
    """Test the sync state manager functionality."""
    print("\nTesting SyncStateManager...")
    
    try:
        from sync_state import SyncStateManager
        
        # Create a temporary state file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_state_file = f.name
        
        # Test state manager
        state_manager = SyncStateManager(temp_state_file)
        
        # Test recording and checking syncs
        test_uid = "test-event-123"
        test_google_id = "google-event-456"
        
        assert not state_manager.is_event_synced(test_uid), "Event should not be synced initially"
        
        state_manager.record_sync(test_uid, test_google_id)
        assert state_manager.is_event_synced(test_uid), "Event should be synced after recording"
        assert state_manager.get_google_event_id(test_uid) == test_google_id, "Google ID should match"
        
        state_manager.save_state()
        
        # Test loading state
        new_state_manager = SyncStateManager(temp_state_file)
        assert new_state_manager.is_event_synced(test_uid), "Event should be synced after loading"
        
        # Clean up
        os.unlink(temp_state_file)
        
        print("✅ SyncStateManager tests passed")
        return True
        
    except Exception as e:
        print(f"❌ SyncStateManager tests failed: {e}")
        return False


def test_configuration():
    """Test configuration validation."""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        
        # Test default values
        assert Config.YANDEX_CALDAV_URL == 'https://caldav.yandex.ru'
        assert Config.GOOGLE_CALENDAR_ID == 'primary'
        assert Config.SYNC_INTERVAL_MINUTES == 30
        assert Config.DAYS_AHEAD == 30
        assert Config.DAYS_BEHIND == 7
        assert Config.LOG_LEVEL == 'INFO'
        
        print("✅ Configuration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration tests failed: {e}")
        return False


def test_google_calendar_format():
    """Test Google Calendar event format conversion."""
    print("\nTesting Google Calendar format conversion...")
    
    try:
        from google_calendar import GoogleCalendarClient
        
        # Create a test client (won't actually connect without credentials)
        client = GoogleCalendarClient()
        
        # Test event data
        test_event = {
            'uid': 'test-uid-123',
            'summary': 'Test Meeting',
            'description': 'Test description',
            'location': 'Test Location',
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(hours=1),
            'is_all_day': False
        }
        
        # Test format conversion
        google_event = client._convert_to_google_format(test_event)
        
        assert google_event['summary'] == 'Test Meeting'
        assert google_event['description'] == 'Test description'
        assert google_event['location'] == 'Test Location'
        assert 'start' in google_event
        assert 'end' in google_event
        assert 'extendedProperties' in google_event
        assert google_event['extendedProperties']['private']['yandex_uid'] == 'test-uid-123'
        
        print("✅ Google Calendar format tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Google Calendar format tests failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Running application tests...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_sync_state_manager,
        test_google_calendar_format
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())