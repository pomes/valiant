package valiant.demo.audit

# A policy suite for checking Valiant audit reports.
#
# Prepare input using:
#   > poetry export --format requirements.txt --output requirements.txt --without-hashes
#   > valiant audit requirements.txt --out json>valiant_audit.json

default allow = false

violations[pkg] = message {
    # Packages not marked as production-ready
    not_mature := {"BASIC005", "BASIC006"}
    findings := input[_].reports.basic.findings[_]
    not_mature[findings.id]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message {
    # Only allow specifically approved licences
    permitted_licenses := {"BSD-3-Clause", "MIT"}
    findings := input[_].reports.spdx.findings[_]
    findings.id == "SPDX001"
    not permitted_licenses[findings.message]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message {
    # All packages must have a properly declared license
    findings := input[_].reports.spdx.findings[_]
    findings.id == "SPDX002"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message  {
    # Any findings from the safety report needs to be raised
    findings := input[_].reports.safety.findings[_]
    findings.id == "SAFETY001"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

allow = true {
    count(violations) == 0
}
