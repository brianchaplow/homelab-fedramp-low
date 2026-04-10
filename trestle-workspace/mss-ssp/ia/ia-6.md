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
  sort-id: ia-06
---

# ia-6 - \[Identification and Authentication\] Authentication Feedback

## Control Statement

Obscure feedback of authentication information during the authentication process to protect the information from possible exploitation and use by unauthorized individuals.

## Control Assessment Objective

the feedback of authentication information is obscured during the authentication process to protect the information from possible exploitation and use by unauthorized individuals.

## Control guidance

Authentication feedback from systems does not provide information that would allow unauthorized individuals to compromise authentication mechanisms. For some types of systems, such as desktops or notebooks with relatively large monitors, the threat (referred to as shoulder surfing) may be significant. For other types of systems, such as mobile devices with small displays, the threat may be less significant and is balanced against the increased likelihood of typographic input errors due to small keyboards. Thus, the means for obscuring authentication feedback is selected accordingly. Obscuring authentication feedback includes displaying asterisks when users type passwords into input devices or displaying feedback for a very limited time before obscuring it.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- For implementation status enter one of: implemented, partial, planned, alternative, not-applicable -->

<!-- Note that the list of rules under ### Rules: is read-only and changes will not be captured after assembly to JSON -->

### This System

All in-boundary service authentication interfaces in the Managed SOC Service obscure password and credential feedback during the authentication process.

For SSH terminal access to all hosts (brisket, haccp, smokehouse, smoker, pitcrew, sear, dojo, regscale), the OpenSSH client provides no visual feedback for passphrase or key-based challenge inputs; echo is suppressed during authentication. For web-based service consoles, every login form masks the password field: Wazuh Dashboard (`https://10.10.20.30:5601`) and Shuffle SOAR (`https://10.10.20.30:3443`) use HTTPS-served login forms with `type="password"` HTML input fields displaying asterisks. OpenCTI (`http://10.10.20.30:8080`), TheHive (`http://10.10.30.22:9000`), Cortex (`http://10.10.30.22:9001`), DefectDojo (`http://10.10.30.27:8080`), and RegScale CE (`http://10.10.30.28`) each use their respective platform login forms with masked password fields. Velociraptor (`https://10.10.20.30:8889`) uses an HTTPS login form with password masking. For pipeline CLI execution, service passwords are sourced from environment variables in `.env`; no password value is echoed to the terminal during `pipelines.sh` execution, and `pipelines/common/config.py` reads credentials from the environment without logging them. All credential masking relies on the browser and terminal platform's standard mechanism, which is the accepted implementation approach under NIST SP 800-53 IA-6 guidance.

#### Implementation Status: implemented

______________________________________________________________________
