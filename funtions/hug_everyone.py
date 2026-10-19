def is_everyone_or_here(who):
    return who is not None and who.strip().lower() in ("@everyone", "@here")