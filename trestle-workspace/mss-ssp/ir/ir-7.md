---
x-trestle-add-props: []
  # Add or modify control properties here
  # Properties may be at the control or part level
  # Add control level properties like this:
  #   - name: ac1_new_prop
  #     value: new property value
  #
  # Add properties to a statement part like this, where "b." is the label of the target statement part
  #   - name: ac1_new_prop
  #     value: new property value
  #     smt-part: b.
  #
x-trestle-global:
  profile:
    title: FedRAMP Rev 5 Low Baseline
    href: trestle://profiles/fedramp-rev5-low/profile.json
  sort-id: ir-07
---

# ir-7 - \[Incident Response\] Incident Response Assistance

## Control Statement

Provide an incident response support resource, integral to the organizational incident response capability, that offers advice and assistance to users of the system for the handling and reporting of incidents.

## Control Assessment Objective

- \[IR-07[01]\] an incident response support resource, integral to the organizational incident response capability, is provided;

- \[IR-07[02]\] the incident response support resource offers advice and assistance to users of the system for the response and reporting of incidents.

## Control guidance

Incident response support resources provided by organizations include help desks, assistance groups, automated ticketing systems to open and track incident response tickets, and access to forensics services or consumer redress services, when required.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

The Managed SOC Service provides an integrated set of IR support resources that collectively serve as the organizational incident response assistance capability. TheHive 4 (pitcrew LXC 200, 10.10.30.22:9000) functions as the primary ticketing and case management platform: every Shuffle WF1 alert becomes a structured case with observable tracking, task assignment, and a full investigation timeline. Cortex 3 (co-located on pitcrew LXC 200, 5 analyzers) provides on-demand automated indicator analysis -- IP reputation, file hash lookup, and domain intelligence -- directly from within any open case, giving the operator immediate analytical assistance without leaving the case management interface. Shuffle SOAR WF1 v2 (brisket:3443/5001) delivers pre-analysis advice with each alert: AbuseIPDB confidence score, Cloudflare block decision, and Wazuh rule classification are posted to Discord #soc-alerts before the operator opens TheHive, reducing investigation bootstrap time. Velociraptor v0.75.3 (brisket:8889, 7 enrolled clients) provides endpoint forensics assistance -- process lists, network connections, file system timelines, and memory artifacts -- for rapid artifact collection across in-boundary and supporting hosts. Ollama qwen3:8b (brisket:11434) augments IR assistance in two ways: the Logstash `zeek-enrichment.conf` Stage 5 calls the LLM (rate-limited to 10/min shared bucket, power-capped at 40W per ADR 0005 thermal hardening) to classify novel network events; WF10 (cron 0530) generates a nightly narrative briefing via `$discord_webhook_briefing` summarizing the previous 24 hours of alerts for morning review. All resources are available on-network at all times; there is no external-facing IR assistance interface, consistent with the single-operator homelab model.

#### Implementation Status: implemented

______________________________________________________________________
