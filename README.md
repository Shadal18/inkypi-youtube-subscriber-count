# InkyPi YouTube Subscriber Count

A custom InkyPi plugin that shows a YouTube channel subscriber count on an e-paper display with a clean, glanceable layout and simple channel-based configuration.

## Install

Use the InkyPi plugin installer with the plugin ID and this repository URL, following the install pattern shown by the official InkyPi plugin template.

```bash
inkypi plugin install youtube_subscriber_count https://github.com/shadal18/inkypi-youtube-subscriber-count
```

## Update

To update the plugin on your InkyPi device:

1. SSH into your InkyPi host.
2. Change into the plugin directory:
   ```bash
   cd ~/InkyPi/src/plugins/youtube_subscriber_count
   ```
3. Run this update command:
   ```bash
   git pull origin main && \
   if [ -d youtube_subs ]; then \
     shopt -s dotglob nullglob && \
     mv youtube_subscriber_count/* . && \
     rmdir youtube_subscriber_count; \
   fi && \
   sudo systemctl restart inkypi.service
   ```

If you don’t see your changes after updating:

- Confirm you are in the correct plugin folder.
- Clear your browser cache or hard refresh the InkyPi web UI.
- Check the InkyPi logs for any plugin errors.

## Requirements

- A working InkyPi installation with plugin support.
- A valid YouTube Data API key with access to YouTube Data API v3.
- A YouTube channel ID for the channel you want to display.
- Network access from the InkyPi device to the YouTube Data API.

## Features

This plugin is an extension for the InkyPi e-paper display frame and includes the following features.

- Shows YouTube subscriber count for a selected channel.
- Uses the YouTube channel ID as the lookup target.
- Supports a custom header label such as `SUBSCRIBERS`.
- Formats subscriber count with thousands separators for readability.
- Clean layout optimized for quick glance reading on e-paper.
- Uses the YouTube channel statistics endpoint as the data source.

## Settings

The plugin settings page lets you customize:

- YouTube channel ID.
- Custom subscribers text.

## API Key Setup

This plugin requires a YouTube API key.

To add the key in InkyPi:

1. Open the InkyPi front page.
2. Click the **key icon**.
3. Add a new key named `YOUTUBE_API_KEY`.
4. Paste in your YouTube API key.
5. Save it.
6. Restart InkyPi if needed.

## Repository

GitHub repository:

[https://github.com/shadal18/inkypi-youtube-subscriber-count](https://github.com/shadal18/inkypi-youtube-subscriber-count)

## Screenshots

- Main plugin display showing the subscriber count.
- Plugin settings screen.

<p align="center">
  <img src="screenshots/example.png" width="45%" />
  <img src="screenshots/settings.png" width="45%" />
</p>
