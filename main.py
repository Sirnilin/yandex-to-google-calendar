#!/usr/bin/env python3
"""Main application for Yandex to Google Calendar synchronization."""

import logging
import sys
import time
import schedule
from typing import NoReturn

from src.synchronizer import CalendarSynchronizer
from src.config import Config


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('sync.log')
        ]
    )


def run_sync() -> None:
    """Run a single synchronization cycle."""
    logger = logging.getLogger(__name__)
    
    try:
        synchronizer = CalendarSynchronizer()
        stats = synchronizer.sync()
        
        logger.info(f"Sync completed successfully: {stats}")
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")


def run_continuous() -> NoReturn:
    """Run continuous synchronization based on configured interval."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting continuous sync every {Config.SYNC_INTERVAL_MINUTES} minutes")
    
    # Schedule the sync job
    schedule.every(Config.SYNC_INTERVAL_MINUTES).minutes.do(run_sync)
    
    # Run initial sync
    run_sync()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def main() -> None:
    """Main entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Yandex to Google Calendar Sync starting...")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'once':
            logger.info("Running single sync")
            run_sync()
        elif command == 'continuous':
            logger.info("Running continuous sync")
            run_continuous()
        else:
            print("Usage: python main.py [once|continuous]")
            print("  once       - Run synchronization once and exit")
            print("  continuous - Run continuous synchronization (default)")
            sys.exit(1)
    else:
        # Default to continuous mode
        run_continuous()


if __name__ == '__main__':
    main()