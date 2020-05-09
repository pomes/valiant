package valiant.demo.audit

test_unknown_licence {
    count(violations) == 1 with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX002",
                            "coordinates": {
                                "name": "test-package",
                                "version": "0.1.0"
                            },
                            "message": "Test message"
                        }
                    ]
                }
            }
        }
    ]
}

test_approved_licence {
    count(violations) == 0 with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "coordinates": {
                                "name": "test-package",
                                "version": "0.1.0"
                            },
                            "message": "MIT"
                        }
                    ]
                }
            }
        }
    ]
}

test_unapproved_licence {
    count(violations) == 1 with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "coordinates": {
                                "name": "test-package",
                                "version": "0.1.0"
                            },
                            "message": "GPL"
                        }
                    ]
                }
            }
        }
    ]
}
