# Semu Frame Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Special agent that queries a SEMU single-sensor device over its HTTPS API and produces a single `Framerate` service which reports the measured frames per second plus the illumination status.

## How it works

1. The special agent calls `https://<host>/api/v5/singlesensor/status` using HTTP Basic authentication (TLS certificate verification is disabled).
2. It prints the JSON response as key/value pairs under the `<<<semu_frames>>>` section.
3. The `semu_frames` check parses the section, computes a rate on `frames_processed` via `get_rate()` and evaluates lower levels on that rate. It also reports the current `illumination` value.

### Example agent output

```text
<<<semu_frames>>>
mac_address D8:80:39:D3:DE:77
frames_processed 8354128
illumination SUFFICIENT
measured_sensor_direction [0.00884352, -0.00114911, -0.99996]
measured_alpha_deg -0.0658392
measured_beta_deg -0.506703
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/semu/libexec/agent_semu` | Special agent (`host`, `user`, `password` as positional args). |
| `src/semu/server_side_calls/agent_semu.py` | Server-side call wiring. |
| `src/semu/rulesets/ruleset.py` | WATO rules for the special agent and the framerate check. |
| `src/semu/agent_based/frames.py` | Section parser and `semu_frames` check plugin. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a Checkmk host for the SEMU device.
3. Configure the *SEMU Framerate* special agent rule with credentials.
4. Run service discovery.

## Configuration

Rule: **Setup -> Agents -> Other integrations -> SEMU Framerate**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `username` | String | HTTP Basic user. |
| `password` | Password | HTTP Basic password. |

Rule: **Parameters for discovered services -> Semu Framerate**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `levels` | Lower levels (frames/s) | WARN/CRIT when the rate drops below the given thresholds. Default `(10, 5)`. |

## Services & metrics

- **Service:** `Framerate`
- **Metric:** `frames` (frames per second, derived from `frames_processed` via rate calculation)
- Illumination value is reported as OK result text.

## Known limitations

- TLS verification is disabled in the agent (`verify=False`).
- Only a single sensor endpoint is queried; multi-sensor SEMU devices would need an extension.
