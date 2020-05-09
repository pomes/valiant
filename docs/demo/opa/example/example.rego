package valiant.demo.example

# Various OPA constructs to demonstrate usage
#
# Example call:
#   ./opa eval --data example/ --input valiant_audit.json --format pretty  'data.valiant.demo.example'

package_version[pkg] = version {
    # Lists the packages and their versions
    # ./opa eval --data example/ --input valiant_audit.json --format pretty  'data.valiant.demo.example.package_version[pkg]'
    pkgs := input[_]
    pkg := pkgs.metadata.name
    version := pkgs.metadata.version
}

all_findings := { id |
    # Display a set of all reported Valiant finding codes
    # ./opa eval --data example/ --input valiant_audit.json --format pretty  'data.valiant.demo.example.all_findings'
    findings := input[_].reports[_].findings[_]
    id := findings.id
}

findings_by_package[pkg] = findings {
    # Provides a listing of findings per package
    # ./opa eval --data example/ --input valiant_audit.json --format pretty  'data.valiant.demo.example.findings_by_package[pkg]'
    pkgs := input[_]
    pkg := pkgs.metadata.name
    pkg_version := pkgs.metadata.version
    findings := { finding |
        f := input[_].reports[_].findings[_]
        f.coordinates.name == pkg
        f.coordinates.version == pkg_version
        finding := f.id
    }
}
