package valiant.demo.audit

test_no_vulnerabilities {
    count(violations) == 0 with input as [
        {
            "reports": {
                "safety": {
                    "findings": []
                }
            }
        }
    ]
}

test_single_vulnerability {
    count(violations) == 1 with input as [
        {
            "reports": {
                "safety": {
                    "findings": [
                        {
                            "id": "SAFETY001",
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

test_single_vulnerability {
    count(violations) == 1 with input as [
        {
            "reports": {
                "safety": {
                    "findings": []
                }
            }
        },
        {
            "reports": {
                "safety": {
                    "findings": [
                        {
                            "id": "SAFETY001",
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

test_multiple_vulnerabilities {
    count(violations) == 2 with input as [
        {
            "reports": {
                "safety": {
                    "findings": []
                }
            }
        },
        {
            "reports": {
                "safety": {
                    "findings": [
                        {
                            "id": "SAFETY001",
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
                "safety": {
                    "findings": [
                        {
                            "id": "SAFETY001",
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
