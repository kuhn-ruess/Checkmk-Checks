# Alertmanager with Severity Mapping

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

Drop-in replacement for the built-in Checkmk Alertmanager check that adds severity remapping and lets you drive service state from the alert severity instead of only the `firing` state. Works for both alert rules and alert groups from version 1.4 of the plugin onwards.

## How it works

The plugin ships a replacement `collection/agent_based/alertmanager.py` and an extended ruleset under `kr_alertmanager/rulesets/alertmanager.py`. The ruleset exposes the normal Alertmanager discovery options (grouping rules into group services, minimum rule count, etc.) and adds a severity mapping so that arbitrary custom severities coming from Prometheus Alertmanager can be mapped to the Checkmk states OK / WARN / CRIT / UNKNOWN.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/kr_alertmanager/rulesets/alertmanager.py` | Extended WATO ruleset with severity remapping. |
| `src/cmk_plugins/collection/agent_based/alertmanager.py` | Replacement check plugin that overrides the shipped one. |

## Installation

1. Install the MKP on the Checkmk site.
2. Enable the Alertmanager special agent rule as usual and configure severity mapping in the extended ruleset.

### Checkmk 2.3

The shipped Alertmanager plugin must be removed manually, because the package only overrides one of the two files. Example Ansible task:

```yaml
- hosts: all
  gather_facts: false
  tasks:
    - name: Delete shipped Alertmanager check
      ansible.builtin.file:
        path: "{{ item }}"
        state: absent
      loop:
        - /opt/omd/versions/{{ cmk_version }}.cee/lib/python3/cmk/base/plugins/agent_based/alertmanager.py
        - /opt/omd/versions/{{ cmk_version }}.cee/lib/python3/cmk/plugins/collection/agent_based/alertmanager.py
      become: true
```

### Checkmk 2.4

No manual cleanup required. The overrides from the MKP take precedence out of the box.

## Known limitations

- Overrides a built-in Checkmk plugin. A Checkmk upgrade that changes the shipped Alertmanager plugin may require updating this package.
