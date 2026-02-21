def parse_amount(value_str, strict=False):
    clean = value_str.strip()

    if clean == "":
        if strict:
            print("Amount missing")
            raise SystemExit(1)
        return None
    
    try:
        number = float(clean)
    except ValueError:
        if strict:
            print(f"Invalid entry: {clean}")
            raise SystemExit(1)
        else:
            print(f"Skipping invalid entry: {clean}")
            return None
        
    if number < 0:
        if strict:
            print("Amounts can't be negative")
            raise SystemExit(1)
        else:
            print(f"Skipping negative value: {number}")
            return None
        
    
    return number