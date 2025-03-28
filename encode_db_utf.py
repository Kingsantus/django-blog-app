with open("mysite_data.json", "rb") as f:
    content = f.read().decode("utf-8", errors="replace")

with open("mysite_data_fixed.json", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed file saved as mysite_data_fixed.json")
