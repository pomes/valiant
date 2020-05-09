package basic

test_app_allowed {
    allow with input as {"name": "valiant", "license": "MIT"}
}

test_app_not_allowed {
    not allow with input as {"name": "my_app", "license": "BSD-3-Clause"}
}

test_app_not_allowed_missing_license {
    not allow with input as {"name": "my_app"}
}
