def parse_entry(entry: str) -> tuple[str, str]:
    source, destination = (
        entry.replace(" ", "").replace("\t", "").replace("\n", "").split("->")
    )
    return source, destination
