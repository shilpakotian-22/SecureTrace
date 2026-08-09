import hashlib


def recipient_hash(text):

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


def recipient_binary(text):

    fingerprint = recipient_hash(text)

    binary = ""

    for character in fingerprint:

        binary += format(
            int(character, 16),
            "04b"
        )

    return binary


def unicode_fingerprint(recipient):

    return recipient_binary(
        f"UNICODE:{recipient}"
    )


def font_fingerprint(recipient):

    return recipient_binary(
        f"FONT:{recipient}"
    )


def synonym_fingerprint(recipient):

    return recipient_binary(
        f"SYNONYM:{recipient}"
    )