ERRORS = {
    "UNV6248E": "Error establishing client session",
    "UNV6337I": "Incoming OMS client connection"
}
def get_error_message(error_code):
    if error_code in ERRORS:
        return ERRORS[error_code]