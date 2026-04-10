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
  sort-id: ca-02.01
---

# ca-2.1 - \[Assessment, Authorization, and Monitoring\] Independent Assessors

## Control Statement

Employ independent assessors or assessment teams to conduct control assessments.

## Control Assessment Objective

independent assessors or assessment teams are employed to conduct control assessments.

## Control guidance

Independent assessors or assessment teams are individuals or groups who conduct impartial assessments of systems. Impartiality means that assessors are free from any perceived or actual conflicts of interest regarding the development, operation, sustainment, or management of the systems under assessment or the determination of control effectiveness. To achieve impartiality, assessors do not create a mutual or conflicting interest with the organizations where the assessments are being conducted, assess their own work, act as management or employees of the organizations they are serving, or place themselves in positions of advocacy for the organizations acquiring their services.

Independent assessments can be obtained from elements within organizations or be contracted to public or private sector entities outside of organizations. Authorizing officials determine the required level of independence based on the security categories of systems and/or the risk to organizational operations, organizational assets, or individuals. Authorizing officials also determine if the level of assessor independence provides sufficient assurance that the results are sound and can be used to make credible, risk-based decisions. Assessor independence determination includes whether contracted assessment services have sufficient independence, such as when system owners are not directly involved in contracting processes or cannot influence the impartiality of the assessors conducting the assessments. During the system design and development phase, having independent assessors is analogous to having independent SMEs involved in design reviews.

When organizations that own the systems are small or the structures of the organizations require that assessments be conducted by individuals that are in the developmental, operational, or management chain of the system owners, independence in assessment processes can be achieved by ensuring that assessment results are carefully reviewed and analyzed by independent teams of experts to validate the completeness, accuracy, integrity, and reliability of the results. Assessments performed for purposes other than to support authorization decisions are more likely to be useable for such decisions when performed by assessors with sufficient independence, thereby reducing the need to repeat assessments.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

This is a single-person portfolio system owned and operated by Brian Chaplow. Full assessor independence -- a separate organizational entity with no stake in the system -- is not feasible at homelab scale. The control is implemented at a commensurate level through three structural independence mechanisms.

First, `pipelines/ingest/wazuh_vulns.py` ingests vulnerability findings directly from the Wazuh Indexer (OpenSearch at `https://10.10.20.30:9200`) without manual filtering. The scanner result is authoritative: the operator cannot alter the finding data before it enters DefectDojo. Second, `pipelines/push/defectdojo.py` writes findings to DefectDojo (10.10.30.27:8080) as a separate system with a separate credential (`$DD_API_KEY` in `.env`); findings cannot be deleted or modified without explicit DefectDojo API access, creating an audit trail that is independent of the pipeline authoring workflow. Third, the test suite in `tests/` (136 tests after Plan 3 Task 3) provides automated, deterministic verification of every pipeline module -- test failures are objective and not subject to operator override without a code change.

The Gate 3 spot-check documented in `docs/adr/0008-plan-3-pre-execution-realignment.md` applies a 144-point self-review of evidence citations against repo artifacts before SSP publication, reducing the risk of undetected hallucinated citations. This is the closest analog to a third-party review available in a single-operator scope.

The accepted limitation is that true third-party independence is not implemented and no contracted 3PAO assessment exists. This is the honest state for a homelab portfolio; the automated pipeline provides the nearest feasible independence substitute and is identified as such.

#### Implementation Status: partial

______________________________________________________________________
