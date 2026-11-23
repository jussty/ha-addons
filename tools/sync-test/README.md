# Sync test: LEDs vs. speakers

A test track and a procedure for setting the LedFx audio delay, so that audio-reactive LEDs flash
together with the speakers. This matters when they get the same audio through different paths,
for example LedFx via Sendspin and a Sonos speaker via its native protocol in a Music Assistant
*Universal Group*. Music Assistant does not align those, so the speaker's buffer shows up as an
offset.

## Procedure

1. **Generate the track** (Python 3, standard library only):

   ```bash
   python3 make_sync_track.py            # double.wav: two beats 0.25 s apart, every 2 s
   ```

2. **Serve it** to Music Assistant, from any machine it can reach:

   ```bash
   python3 -m http.server 8765 --bind <this-machine's-ip>
   ```

3. **Play it** on the group that contains the speaker and the LedFx player. You can use
   Developer tools → Actions in Home Assistant:

   ```yaml
   action: music_assistant.play_media
   target:
     entity_id: media_player.<your_group>
   data:
     media_id: http://<this-machine's-ip>:8765/double.wav
     media_type: track
   ```

4. **Watch and listen:**
   - Does the double flash come **before** or **after** the double beat?
   - Roughly by how much? The gap within a pair is 250 ms, the period is 2 s.

5. **Adjust:**
   - **LEDs early:** raise LedFx *Settings → Audio → Delay (ms)* by about the offset.
   - **LEDs late:** LedFx can only delay its output, so the fix has to come from the audio side
     instead, for example a smaller buffer or a delay setting on the speaker.

   Changing the delay restarts LedFx's audio stream, and Music Assistant may stop the playback.
   Start the track again after each change.

6. **Check stability:** stop the group, start it again, and look once more. If the offset stays
   the same, the value holds. In our setup, a Sonos Era 100 plus the LedFx add-on, that was
   **500 ms**.

## Patterns

| Pattern | What it shows |
| --- | --- |
| `double` (default) | The direction and the size of the offset, as long as it is below about 1.5 s |
| `click` | One beat per second, good for a quick look. Offsets near 500 ms are ambiguous: early and late look the same. |
