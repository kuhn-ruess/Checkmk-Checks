# Password Age

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p13-blue)
<!-- compatibility-badges:end -->

Monitors when local Linux user passwords are set to expire. The Checkmk
agent plugin runs `chage -l` for a fixed list of users and Checkmk creates
one service per user that reports the days until expiry.

## How it works

1. Shell agent plugin [`password_age.sh`](src/agents/plugins/password_age.sh)
   runs `chage -l <user>` on each configured user and prints the
   `Password expires` line under the `<<<password_age:sep(58)>>>` section,
   using `[[[user]]]` headers.
2. The check plugin parses each header and parses the date (or the literal
   `never` / `does not ...` strings) and creates one service per user.
3. State logic:
   - `never` -> OK, summary `Never expires`
   - `does not ...` -> WARN, summary is the literal message
   - Date -> OK if more than 10 days remain, CRIT within 10 days

Example agent output:

```text
<<<password_age:sep(58)>>>
[[[cmkmon]]]
Password expires          : Jan 01, 2027
[[[root]]]
Password expires          : never
```

## Package contents

| Path | Purpose |
| --- | --- |
| `src/agents/plugins/password_age.sh` | Bash agent plugin that runs `chage -l` for a hardcoded user list (`cmkmon`, `root`). |
| `src/password_age/agent_based/passwort_age.py` | Section parser + check plugin `password_age`. |
| `src/password_age/agent_based/bakery.py` | Agent Bakery hook to deploy the plugin. |
| `src/password_age/rulesets/bakery.py` | WATO AgentConfig ruleset `password_age` for deployment mode. |

## Installation

1. Install the MKP on the Checkmk site.
2. Deploy the agent plugin:
   - **With Bakery:** enable the rule *Setup -> Agents -> Agent rules ->
     password_age: Monitoring Users Password Age (Linux)* and bake the
     agent.
   - **Without Bakery:** copy `src/agents/plugins/password_age.sh` to
     `/usr/lib/check_mk_agent/plugins/` on the target host and make it
     executable.
3. Run service discovery. Services `Password Age: <user>` appear for each
   user block the agent emitted.

## Configuration

Rule: **Setup -> Agents -> Agent rules -> password_age: Monitoring Users
Password Age (Linux)**

| Parameter | Type | Meaning |
| --- | --- | --- |
| `deployment` | `sync` / `cached <time>` / `do_not_deploy` | Choose synchronous deployment, asynchronous deployment with a cache interval, or skip the plug-in entirely. |

There is no ruleset for the check thresholds - the 10 day CRIT threshold
is hardcoded in the check plugin.

## Services & metrics

- **Service:** `Password Age: <user>` - one per user.
- No metrics.

## Known limitations

- The user list is hardcoded in `password_age.sh` (`cmkmon`, `root`) -
  extend the script to monitor more users.
- The 10-day CRIT threshold is hardcoded in the check plugin; there is no
  `check_ruleset_name`.
