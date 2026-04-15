# Sina Inventory

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0-blue)
<!-- compatibility-badges:end -->

HW/SW inventory plugin for secunet SINA Workstations. Parses a JSON blob delivered by a SINA-side agent and writes system, hardware, BIOS, user/token and arbitrary `hwinfo` data into the Checkmk HW/SW inventory tree so that support staff can see background information on a host directly from its inventory view.

## How it works

- Agent section name: `<<<sina_ws>>>` (single JSON line, parsed via `json.loads`).
- Writes fixed attributes:
  - `software/os` — `type=SINA OS`, vendor `secunet`, derived `version` from `hwinfo.sinaVersion`.
  - `hardware/system` — manufacturer, UUID, serial, model from `hwinfo.system*`.
  - `hardware/bios` — BIOS version.
  - `sina` — last dial-in time (formatted from `timestamp`).
- Dynamic collectors walk `hwinfo` (minus the system-level keys used above) and `hardware`, emitting either `Attributes` (for scalars / dicts) or `TableRow` (for lists) under `sina/workstation`.
- SINA tokens are emitted under `sina/token/<username>` — one node per user from `section['users']`, keyed by the user's name before `@`.

## Package contents

| Path | Purpose |
| --- | --- |
| `src/sina_inventory/agent_based/sina_inventory.py` | Agent section `sina_ws` and `InventoryPlugin` writing the inventory tree. |

## Installation

1. Install the MKP on the Checkmk site.
2. Ensure that the SINA workstation delivers a `<<<sina_ws>>>` section with the expected JSON payload (agent-side setup is not part of this package).
3. Run inventory on the host to populate the HW/SW inventory tree.

## Known limitations

- Agent-side data producer is not included; the plugin assumes the JSON payload shape produced by secunet SINA workstations.
- Purely an inventory plugin — no services or metrics are created.
