# Videotext timestamp monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.3.0p9-blue)
<!-- compatibility-badges:end -->

Active check that fetches a teletext/Videotext page over HTTP, extracts a `HH:MM` timestamp with a regular expression, and alerts when the age of that timestamp compared to the current wall-clock time exceeds configurable thresholds.

## How it works

1. `check_videotext` GETs the configured URL (default timeout 30 s).
2. The response body (with newlines stripped) is searched with the configured regex; the first capture group must contain a `HH:MM` value.
3. That time is combined with today's year/month/day and subtracted from `datetime.now()`.
4. The script exits with:
   - `0` (OK) if no warn/crit is reached,
   - `1` (WARN) if the age is `>= warn`,
   - `2` (CRIT) if the age is `>= crit`,
   - `3` (UNKNOWN) if the pattern could not be found.
5. Perfdata `time=<seconds>s;;;;` is always emitted.

Service name is fixed to `Videotext`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/videotext/libexec/check_videotext` | Active check script (Python, uses `requests`). |
| `src/videotext/rulesets/active_check.py` | WATO `ActiveCheck` rule *Videotext timestamp monitoring*. |
| `src/videotext/server_side_calls/active_check.py` | Builds the command line with `-u`, `-p`, `-t`, `-w`, `-c`. |

## Installation

1. Install the MKP on the Checkmk site.
2. Create a *Videotext timestamp monitoring* rule under *Setup > Services > HTTP, TCP, Email... > Videotext timestamp monitoring*.
3. The active check runs from the Checkmk site, no agent deployment is required.

## Configuration

| Parameter | Type | Default | Meaning |
| --- | --- | --- | --- |
| `url` | String (required) | — | Full URL of the videotext page. |
| `pattern` | RegularExpression (required) | `Stand:.*?(\d+:\d+)` | Regex with a single capture group containing `HH:MM`. |
| `timeout` | TimeSpan | 2.5 s (rule), 30 s (script fallback) | HTTP request timeout passed as `-t`. |
| `warn` | TimeSpan | 900 s | Upper WARN threshold on age in seconds. |
| `crit` | TimeSpan | 1200 s | Upper CRIT threshold on age in seconds. |

## Known limitations

- The timestamp is always interpreted with **today's** date, so a page showing `23:58` when the check runs at `00:02` produces a ~24 h diff and false CRIT around midnight.
- `diff.seconds` is used instead of `diff.total_seconds()`; negative diffs (clock skew) and multi-day diffs are not handled correctly.
- Only the first regex match is considered; multi-timestamp pages are not supported.
