package valiant.demo.dependency

default allow = false

violations[pkg] = message {
    # Packages not marked as production-ready
    not_mature := {"BASIC005", "BASIC006"}
    findings := input.reports.basic.findings[_]
    not_mature[findings.id]
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

violations[pkg] = message {
    # All packages must have a properly declared license
    findings := input.reports.spdx.findings[_]
    findings.id == "SPDX002"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := "SPDX002: No licence could be determined."
}

violations[pkg] = message {
    # All packages must have an OSI-approved license
    findings := input.reports.spdx.findings[_]
    findings.id == "SPDX001"; findings.data.is_osi_approved != true
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := "An OSI-approved licence is required."
}

violations[pkg] = message  {
    # Any findings from the safety report needs to be raised
    findings := input.reports.safety.findings[_]
    findings.id == "SAFETY001"
    pkg := concat("::", [findings.coordinates.name, findings.coordinates.version])
    message := concat(": ", [findings.id, findings.message])
}

allow = true {
    count(violations) == 0
}
