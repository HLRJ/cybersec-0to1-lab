# S00 Curriculum Restructure Design

**Date:** 2026-09-17

## Problem

The first S00 lesson was originally implemented as Authorization & Scope before the learner had created any real lab assets. During the first learner run, this caused a false dependency: the repository assumed an imaginary VMware subnet before a Cyber Range existed.

The corrected teaching principle is: **build and verify the lab assets first, then define Scope from the real authorized assets.**

## Decision

Reorder Stage 00 so the learner first builds an isolated VMware Cyber Range, then learns authorization and Scope against that real environment.

### S00-L01 — Build Your Cyber Range

The repository will document the reproducible environment-building flow used in the learner run:

- download Ubuntu Server and Kali from official sources;
- verify SHA256 hashes against the official published checksums;
- create a dedicated VMware Host-Only network with DHCP disabled;
- plan addresses for the Windows host, Ubuntu target, and Kali tester;
- install/configure Ubuntu and import/configure Kali;
- keep Ubuntu/Kali without a default Internet route;
- verify the three-node connectivity matrix;
- verify Internet isolation using an IP target such as `8.8.8.8` rather than a DNS name;
- create baseline snapshots after validation;
- capture troubleshooting learned during the run, including the Kali invisible-cursor issue caused in this case by old VMware virtual hardware compatibility.

The learner's concrete environment is `192.168.77.0/24`, but the public lesson must teach the learner to discover/create and record their own lab subnet instead of assuming `.77` universally.

### S00-L02 — Authorization & Scope

Move the existing Scope lesson from `labs/s00/l01-scope/` to `labs/s00/l02-scope/`.

The lesson must explicitly consume the learner's verified Cyber Range subnet from L01. The sample repository configuration may show `192.168.77.0/24` as the reference implementation, but the prose must state that authorization comes from the learner's actual lab design, not from RFC1918/private-address status.

The deny-by-default target guard and its automated tests remain conceptually unchanged.

## Revised Stage 00 Sequence

1. **S00-L01 — Build Your Cyber Range**
2. **S00-L02 — Authorization & Scope**
3. **S00-L03 — Snapshot / Reset / Recovery**
4. **S00-L04 — Workstation & Toolchain**
5. **S00-L05 — Baseline Telemetry**

No intentional vulnerability is introduced in S00.

## Repository Changes

Expected implementation changes:

- create `labs/s00/l01-cyber-range/README.md`;
- move/rename `labs/s00/l01-scope/` to `labs/s00/l02-scope/`;
- update `README.md`, `CURRICULUM.md`, `docs/CURRICULUM_DESIGN.md`, and `docs/LAB_RULES.md` so numbering and prerequisites agree;
- preserve `scope/lab-scope.yaml`, `scripts/check_lab_target.py`, and the existing Scope tests, changing only references needed by the new lesson number;
- keep CI running the automated Scope tests.

## S00-L01 Gate

A learner passes L01 only after they can provide evidence that:

- the host, Ubuntu, and Kali are on the dedicated lab network and mutually reachable;
- Ubuntu and Kali have no default route to the Internet;
- `ping` or equivalent to an external IP fails because there is no route;
- baseline snapshots exist for the lab VMs;
- the learner can explain why Host-Only plus no default route reduces accidental target exposure.

## Checkpoint and Tag Policy

The already-pushed tag `s00-l01-complete` currently points to the old Scope lesson and is therefore semantically stale after this restructure.

Do **not** silently force-move or rewrite the public tag. Preserve it as historical evidence. The restructure will introduce new unambiguous checkpoint tags after the corrected lessons are completed, using a versioned suffix if necessary (for example `s00-l01-complete-v2` and `s00-l02-complete-v2`). The exact final tag names will be chosen during implementation and documented in the PR.

## Troubleshooting Content to Preserve

The L01 lesson should include concise troubleshooting notes derived from the real learner run:

- official ISO/archive hash verification before installation;
- VMware Host-Only adapter versus NAT distinction;
- DHCP-off static addressing;
- Ubuntu static address with gateway/DNS intentionally blank for isolation;
- Kali NetworkManager static address with `ipv4.never-default yes`;
- SSH reachability as a useful service-level validation;
- Kali invisible mouse cursor: in this learner run, `open-vm-tools` was installed and disabling 3D acceleration did not fix it; upgrading the imported VM from old virtual hardware compatibility (`virtualHW.version = "8"`) resolved the issue. Present this as a case-specific root cause, not a universal rule.

## Non-Goals

This restructure does not add vulnerable services, scanning exercises, exploitation, Active Directory, or Internet-facing targets. It does not make the learner's physical LAN part of Scope.

## Acceptance Criteria

The restructure is complete when:

- every Stage 00 document agrees on the new L01/L02 numbering;
- the environment-building lesson is reproducible without relying on this chat history;
- the public lesson does not hard-code `192.168.77.0/24` as a mandatory learner subnet;
- Scope remains deny-by-default and tests still pass;
- CI passes on the pull request;
- no old lesson path or wording incorrectly claims Scope is S00-L01.
