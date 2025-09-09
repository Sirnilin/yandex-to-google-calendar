# Yandex to Google Calendar Sync - Development Notes

## Architecture Overview

The application consists of several key components:

### Core Modules

1. **config.py** - Configuration management using environment variables
2. **yandex_calendar.py** - Yandex Calendar CalDAV client
3. **google_calendar.py** - Google Calendar API client
4. **sync_state.py** - State management for tracking synced events
5. **synchronizer.py** - Main synchronization logic
6. **main.py** - Application entry point with scheduling

### Key Features

- **CalDAV Integration**: Uses standard CalDAV protocol to access Yandex Calendar
- **OAuth2 Authentication**: Secure Google Calendar API access
- **Duplicate Prevention**: Tracks synced events to avoid duplicates
- **Error Handling**: Robust error handling and logging
- **Configurable Sync**: Customizable sync intervals and date ranges
- **Docker Support**: Complete containerization for server deployment

### Data Flow

1. **Fetch Events**: Retrieve events from Yandex Calendar via CalDAV
2. **Check State**: Determine which events are already synced
3. **Create/Update**: Sync new events or update existing ones in Google Calendar
4. **Track State**: Record sync mappings for future reference
5. **Schedule**: Wait for next sync interval

### Configuration

All configuration is handled through environment variables:

- **YANDEX_USERNAME**: Yandex account email
- **YANDEX_PASSWORD**: App-specific password
- **GOOGLE_CALENDAR_ID**: Target Google Calendar
- **SYNC_INTERVAL_MINUTES**: How often to sync
- **DAYS_AHEAD/BEHIND**: Date range for sync

### Security Considerations

- Credentials are stored in environment variables
- Google OAuth tokens are managed securely
- App passwords are recommended for Yandex access
- No sensitive data in logs

### Deployment Options

1. **Local Development**: Direct Python execution
2. **Docker Container**: Single container deployment
3. **Docker Compose**: Full stack with volumes and networks
4. **Server Deployment**: Continuous operation with restart policies

### Error Handling

- Connection failures are logged and retried
- Individual event errors don't stop the sync
- State corruption is handled gracefully
- Invalid events are skipped with warnings

### Testing

The application includes comprehensive tests:

- Import validation
- Configuration testing
- State management verification
- Event format conversion

### Future Enhancements

Potential improvements:
- Support for multiple Yandex calendars
- Bidirectional synchronization
- Calendar selection UI
- Advanced filtering options
- Webhook-based real-time sync
- Event conflict resolution
- Backup and restore functionality

### Dependencies

Key libraries:
- **caldav**: CalDAV protocol implementation
- **google-api-python-client**: Google Calendar API
- **schedule**: Task scheduling
- **python-dotenv**: Environment variable management
- **pytz**: Timezone handling

### Troubleshooting

Common issues:
1. **Yandex Connection**: Check app password creation
2. **Google Auth**: Verify OAuth setup and credentials.json
3. **Docker Build**: SSL certificate issues in sandbox environments
4. **Timezone Issues**: Events may appear at wrong times without proper timezone handling