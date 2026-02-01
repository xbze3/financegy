def safe_text(parent, class_name):
    cell = parent.find("td", class_=class_name)
    return cell.get_text(strip=True) if cell else None
