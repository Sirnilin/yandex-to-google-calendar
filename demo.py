#!/usr/bin/env python3
"""Demo script showing the application functionality without real credentials."""

import logging
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config


def demo_configuration():
    """Demo configuration validation."""
    print("=== Configuration Demo ===")
    print(f"Yandex CalDAV URL: {Config.YANDEX_CALDAV_URL}")
    print(f"Google Calendar ID: {Config.GOOGLE_CALENDAR_ID}")
    print(f"Sync Interval: {Config.SYNC_INTERVAL_MINUTES} minutes")
    print(f"Days Ahead: {Config.DAYS_AHEAD}")
    print(f"Days Behind: {Config.DAYS_BEHIND}")
    print(f"Log Level: {Config.LOG_LEVEL}")
    print()


def demo_event_structure():
    """Demo event data structure."""
    print("=== Event Data Structure Demo ===")
    
    # Sample event data that would come from Yandex Calendar
    sample_event = {
        'uid': 'sample-event-uid-123',
        'summary': 'Important Meeting',
        'description': 'Discussion about project milestones',
        'location': 'Conference Room A',
        'start_time': datetime.now(),
        'end_time': datetime.now() + timedelta(hours=1),
        'is_all_day': False,
        'raw_event': 'VEVENT...ICAL_DATA...'
    }
    
    print("Sample Yandex Calendar Event:")
    for key, value in sample_event.items():
        if key != 'raw_event':  # Skip raw data
            print(f"  {key}: {value}")
    print()


def demo_sync_logic():
    """Demo synchronization logic."""
    print("=== Sync Logic Demo ===")
    
    # Simulate sync process
    print("1. Connect to Yandex Calendar (CalDAV)")
    print("2. Fetch events from date range")
    print("3. For each event:")
    print("   - Check if already synced")
    print("   - If new: create in Google Calendar")
    print("   - If exists: update if needed")
    print("   - Record sync in state file")
    print("4. Save sync state")
    print("5. Schedule next sync")
    print()


def demo_docker_deployment():
    """Demo Docker deployment info."""
    print("=== Docker Deployment Demo ===")
    print("To deploy with Docker:")
    print("1. Copy .env.example to .env and fill with credentials")
    print("2. Place Google credentials.json in data/ folder")
    print("3. Run: docker-compose up -d")
    print("4. Monitor with: docker-compose logs -f")
    print()
    
    print("Container features:")
    print("- Automatic restart on failure")
    print("- Persistent data storage")
    print("- Health checks")
    print("- Configurable sync intervals")
    print()


def main():
    """Run the demo."""
    print("🚀 Yandex to Google Calendar Sync - Demo Mode")
    print("=" * 50)
    print()
    
    demo_configuration()
    demo_event_structure()
    demo_sync_logic()
    demo_docker_deployment()
    
    print("✅ Demo completed successfully!")
    print("\nTo run the actual sync:")
    print("1. Set up Yandex and Google credentials")
    print("2. Run: python main.py once (for single sync)")
    print("3. Run: python main.py continuous (for ongoing sync)")


if __name__ == '__main__':
    main()