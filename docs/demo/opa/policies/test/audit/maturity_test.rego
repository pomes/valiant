package valiant.demo.audit

test_maturity {
    count(violations) == 2 with input as [
        {
            "reports": {
                "basic": {
                    "findings": [
                        {
                            "id": "BASIC005",
                            "coordinates": {
                                "name": "test-package",
                                "version": "0.1.0"
                            },
                            "message": "Test message"
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "basic": {
                    "findings": [
                        {
                            "id": "BASIC006",
                            "coordinates": {
                                "name": "test-package-2",
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

test_devlopment_package {
    count(violations) == 1 with input as [
        {
            "reports": {
                "basic": {
                    "findings": [
                        {
                            "id": "BASIC005",
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

test_inactive_package {
    count(violations) == 1 with input as [
        {
            "reports": {
                "basic": {
                    "findings": [
                        {
                            "id": "BASIC006",
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
