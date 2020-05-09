package valiant.demo.dependency

test_no_licence {
    count(violations) == 1 with input as {
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
}

test_osi_licence {
    count(violations) == 0 with input as {
        "reports": {
            "spdx": {
                "findings": [
                    {
                        "id": "SPDX001",
                        "coordinates": {
                            "name": "test-package",
                            "version": "0.1.0"
                        },
                        "data": {
                            "is_osi_approved": true
                        },
                        "message": "Test message"
                    }
                ]
            }
        }
    }
}

test_non_osi_licence {
    count(violations) == 1 with input as {
        "reports": {
            "spdx": {
                "findings": [
                    {
                        "id": "SPDX001",
                        "coordinates": {
                            "name": "test-package",
                            "version": "0.1.0"
                        },
                        "data": {
                            "is_osi_approved": false
                        },
                        "message": "Test message"
                    }
                ]
            }
        }
    }
}
