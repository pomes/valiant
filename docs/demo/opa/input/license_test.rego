package valiant.demo

test_allow_permitted_license {
    allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "BSD-3-Clause",
                        }
                    ]
                }
            }
        }
    ]
}


test_allow_permitted_licenses {
    allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "BSD-3-Clause",
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "MIT",
                        }
                    ]
                }
            }
        }
    ]
}

test_fail_not_permitted_licenses {
    not allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "BSD-3-Clause",
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "GPL",
                        }
                    ]
                }
            }
        }
    ]
}


test_fail_missing_licenses {
    not allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX002",
                            "coordinates": {
                                "name": "Test"
                            }
                        }
                    ]
                }
            }
        }
    ]
}

test_fail_missing_licenses {
    not allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "BSD-3-Clause",
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX002",
                            "coordinates": {
                                "name": "Test"
                            }
                        }
                    ]
                }
            }
        }
    ]
}

test_fail_not_permitted_and_missing_licenses {
    not allow_licenses with input as [
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "BSD-3-Clause",
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX001",
                            "message": "GPL",
                        }
                    ]
                }
            }
        },
        {
            "reports": {
                "spdx": {
                    "findings": [
                        {
                            "id": "SPDX002",
                            "coordinates": {
                                "name": "Test"
                            }
                        }
                    ]
                }
            }
        }
    ]
}
