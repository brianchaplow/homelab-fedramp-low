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
  sort-id: pl-04.01
---

# pl-4.1 - \[Planning\] Social Media and External Site/Application Usage Restrictions

## Control Statement

Include in the rules of behavior, restrictions on:

- \[(a)\] Use of social media, social networking sites, and external sites/applications;

- \[(b)\] Posting organizational information on public websites; and

- \[(c)\] Use of organization-provided identifiers (e.g., email addresses) and authentication secrets (e.g., passwords) for creating accounts on external sites/applications.

## Control Assessment Objective

- \[PL-04(01)(a)\] the rules of behavior include restrictions on the use of social media, social networking sites, and external sites/applications;

- \[PL-04(01)(b)\] the rules of behavior include restrictions on posting organizational information on public websites;

- \[PL-04(01)(c)\] the rules of behavior include restrictions on the use of organization-provided identifiers (e.g., email addresses) and authentication secrets (e.g., passwords) for creating accounts on external sites/applications.

## Control guidance

Social media, social networking, and external site/application usage restrictions address rules of behavior related to the use of social media, social networking, and external sites when organizational personnel are using such sites for official duties or in the conduct of official business, when organizational information is involved in social media and social networking transactions, and when personnel access social media and networking sites from organizational systems. Organizations also address specific rules that prevent unauthorized entities from obtaining non-public organizational information from social media and networking sites either directly or through inference. Non-public information includes personally identifiable information and system account information.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

No standalone Rules of Behavior document exists that explicitly enumerates the three social-media restriction categories. In practice, restriction (c) -- organizational identifiers on external accounts -- is satisfied by `/c/Projects/CLAUDE.md` §Credentials ("All credentials are in `.env` (gitignored)") and §Conventions ("NEVER hardcode credentials"), which prevent organizational secrets from being posted to external sites or used to create third-party accounts. The public GitHub repo (`github.com/brianchaplow/homelab-fedramp-low`) enforces restriction (b) by excluding all secrets via `.gitignore`. ADR 0001 §RegScale CE EULA §2(ix) ("No publishing circumvention info") constitutes an acknowledged external-site posting restriction. No organizational email identifiers (e.g., `.gov` addresses) are used in this system -- `deploy/regscale/README.md` and `deploy/defectdojo/README.md` confirm admin accounts are not linked to organizational email.

The status is partial because no formal RoB document enumerates restrictions (a) social media use, (b) posting organizational information, and (c) organizational identifiers -- the restrictions exist by convention but not in a disseminated policy artifact.

#### Implementation Status: partial

______________________________________________________________________
