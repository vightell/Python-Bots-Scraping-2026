with open("NOTES.md", "r", encoding="utf-8") as file:
    content = file.read()

start = content.find("## Day 3")
end = content.find("## Day 6")
print(content[start:end])