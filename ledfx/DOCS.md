# LedFx

[LedFx](https://github.com/LedFx/LedFx) turns audio into LED effects and sends them to WLED, ESPHome
(`wled`/`e131` effects), E1.31, DDP and other devices on the network.

This add-on runs the upstream LedFx image unchanged, except for one thing: there is no PulseAudio
and no sound card. Audio comes over the network from **Music Assistant via Sendspin**. LedFx joins
Music Assistant as a Sendspin player. Anything you play to that player, or to a group that
contains it, drives the LEDs.

## Setup

1. Start the add-on and open the web interface (port 8888).
2. **Settings → Sendspin:** add a server with URL `ws://127.0.0.1:8927/sendspin`. Music Assistant
   runs on the same host. Discovery may offer a different address, because Music Assistant
   announces its `publish_ip`.
3. **Settings → Audio:** pick `SENDSPIN: <server name>` as the audio device.
   - **LedFx 2.2.1 bug:** On a host without any sound device, the audio device list fails with
     `tuple index out of range` until a device has been selected once.
   - Select the Sendspin device through the API instead. With a single Sendspin server it is
     index `0`:

     ```bash
     curl -X PUT http://<ha-host>:8888/api/audio/devices -H 'Content-Type: application/json' \
          -d '{"audio_device": 0}'
     ```
4. Add your devices and pick an effect.
5. In Music Assistant, the player shows up under the client name configured in step 2.
   - Play to it directly, or add it to a group.
   - To keep the LEDs in step with speakers that use another protocol (Sonos, AirPlay,
     Chromecast), put both in a *Universal Group*.
   - If the LEDs run ahead of the speakers, set **Settings → Audio → Delay (ms)**.

## Notes

- **Do not `POST /api/config`.** LedFx treats it as an import and replaces the whole configuration.
  To change single values, use `PUT /api/config`. LedFx writes a backup (`config_backup_*.json`)
  before an import.
- **`PUT /api/config` for `audio`:** always include `audio_device`, for example
  `{"audio": {"audio_device": 0, "delay_ms": 500}}`. Without it, LedFx looks for a default device
  and hits the bug above. `audio_device_name` is rejected as an unknown key.
- **Changing the audio delay restarts the audio stream.** Music Assistant may stop the playback;
  start it again. If the LEDs stay dark afterwards, restart the add-on.
- **UDP devices:** turn off *Minimise Traffic* for receivers with a short timeout, such as the
  ESPHome `wled` effect. Otherwise a static frame stops being sent and the receiver blanks.
- **No authentication:** The web interface has none and listens on the host network, port 8888.
  Only use it on a trusted network.
- **Persistent data:** The configuration lives in the add-on's `/data/ledfx` and is included in
  Home Assistant backups.

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `verbose` | `false` | Log level INFO instead of WARNING |
