def validate_code(code: str) -> bool:
    if not code:
        return False

    if not code.split('\n')[0].strip().startswith('def generate_slides'):
        return False

    if 'return' not in code.split('\n')[-1]:
        return False

    if 'import' in code:
        return False

    if 'from' in code:
        return False

    return True
