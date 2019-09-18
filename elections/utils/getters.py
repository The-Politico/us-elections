def get_party(party_code, parties):
    if not party_code:
        return None
    matched = list(
        filter(lambda d: d.ap_code.lower() == party_code.lower(), parties)
    )
    if len(matched) > 0:
        return matched[0]
    return None
