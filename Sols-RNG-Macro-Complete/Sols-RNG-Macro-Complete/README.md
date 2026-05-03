# MultiFMacro - Sols RNG Macro UI

A powerful Python/Tkinter GUI macro for Sols RNG with Discord webhook notifications, AFK mode, multi-account support, and advanced biome/aura tracking.

**Made by Coder-masa**

## Features

✨ **User Interface**
- Multi-page navigation system (9 pages)
- 6 built-in themes + random color generator
- Live macro status badge
- Real-time RNG event simulation
- Responsive buttons and interactive controls

🎮 **Macro Functionality**
- Start, Pause, Stop controls
- AFK Mode toggle
- Multi-account support
- Aura and Biome notification system
- Discord webhook integration

⚙️ **Configuration**
- Webhook URL configuration
- Private server support
- Discord ID settings
- Roblox username management
- Persistent config saving (JSON)

📱 **Pages**
1. **Webhook** - Main panel with configuration and biome alerts
2. **Aura** - Aura scan and color settings
3. **Detections** - Entity scan and alert controls
4. **Antikick** - Anti-kick protection options
5. **Fishing** - Fishing automation settings
6. **Leaderboard** - Weekly/Daily/All-Time/Friends rankings
7. **Remote** - Remote spy and command execution
8. **UI** - Theme selection and accent mode
9. **Credits** - About and version info

## Installation

### Requirements
- Python 3.8+
- No external packages required (uses standard library only)

### Setup

1. **Download and Extract**
   ```bash
   # Extract this folder to your desired location
   ```

2. **Run the Macro**
   ```bash
   python Codez-1.py
   ```

## Configuration

### Discord Webhook Setup

1. Open the macro and navigate to the **Webhook** page
2. Enter your Discord webhook URL in the "Webhook URL" field
3. Configure optional settings:
   - **Private Server**: Your private server ID
   - **Discord ID**: Your Discord user ID
   - **Roblox User**: Your Roblox username

4. Enable features:
   - **AFK Mode**: Run macro while AFK
   - **Multiaccount**: Support multiple accounts
   - **Aura / Biome Notifications**: Get alerts for specific biomes

5. Select biomes to monitor from the "Biome Ping" panel

6. Click **Test Webhook** to verify setup

### Theme Selection

- Choose from 6 pre-built themes: Red, Black, White, Orange, Pink, Blue
- Click **Random Colors** to generate a custom theme
- Theme preference is saved automatically

### Biome Selection

Check the biomes you want to receive notifications for:
- Corruption, Eggland, Heaven, Hell, Null, Rainy
- Sand Storm, Singularity, Snowy, Starfall, Windy
- Cyberspace, Dreamspace, Glitched

## Usage

### Starting the Macro

1. Configure your webhook and settings
2. Click **Start** to begin the RNG macro
3. Monitor the status bar for real-time events
4. Click **Pause** to pause/resume, **Stop** to terminate

### Viewing Logs

- Check the log panel at the bottom of the Webhook page
- View timestamps and action details
- Scroll through history to track macro activity

### Saving Configuration

- Click **Save Config** to persist your settings
- Config is automatically loaded on next launch
- Config file: `macro_config.json`

## File Structure

```
Sols-RNG-Macro-Complete/
├── Codez-1.py          # Main macro script
├── README.md           # This file
├── requirements.txt    # Dependencies (none for core functionality)
└── macro_config.json   # Auto-generated config file
```

## Troubleshooting

### Webhook Not Working
- Verify your Discord webhook URL is correct
- Ensure the Discord channel still exists
- Check that the webhook has permission to send messages

### Theme Not Applying
- Restart the macro
- Try selecting a different theme first, then your desired theme

### Config Not Saving
- Ensure you have write permissions in the script directory
- The `macro_config.json` file should be created automatically

## Advanced Features

### RNG Event Types
The macro simulates 8 different RNG event types:
- Rare spawn rolled
- Perfect RNG result found
- Aura shimmer detected
- Biome signal active
- Lucky RNG check succeeded
- Stream event triggered
- Ghost RNG pulse
- Hidden treasure ping

### Webhook Notifications
Events that trigger Discord notifications:
- Macro start/stop/pause/resume
- Webhook test messages
- Aura/Biome detection alerts
- Remote spy activation

### Page-Specific Actions

Each page supports interactive buttons that update in real-time:
- **Aura Page**: Toggle scan, change color, set range
- **Detections Page**: Entity scan, alert sound, distance check
- **Antikick Page**: Enable guard, safe mode, session watch
- **Fishing Page**: Auto-fish toggle, bait selection, catch tracking
- **Leaderboard Page**: Switch between ranking views
- **Remote Page**: Spy toggle, command execution, request log
- **UI Page**: Theme picker, accent mode, reset UI

## Notes

- The macro runs in a background thread to keep UI responsive
- Config persistence ensures settings are retained between sessions
- Discord notifications require a valid webhook URL
- The GUI is optimized for 1040x640 resolution

## Support

For issues or feature requests, ensure:
1. Python 3.8+ is installed
2. You have internet connection for Discord notifications
3. Your Discord webhook URL is valid and active

**Version**: 1.0  
**Build**: 2026  
**Author**: Coder-masa

---

*This macro UI is provided as-is. Use responsibly.*
