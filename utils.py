def parse_amount(value_str, strict=False) -> float:
    clean = value_str.strip()

    if clean == "":
        return None
    
    try:
        number = float(clean)
    except ValueError:
        if strict == True:
            print(f"Invalid entry: {clean}")
            raise SystemExit(1)
        else:
            print(f"Skipping invalid entry: {clean}")
            return None
    
    return number