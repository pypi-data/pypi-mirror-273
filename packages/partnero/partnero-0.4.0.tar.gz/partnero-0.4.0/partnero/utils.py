def validate_email(email):
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Provided email is not a valid email address")


def validate_key(key, key_name="key"):
    if not key or not isinstance(key, str):
        raise ValueError(f"The {key_name} must be a non-empty string")
