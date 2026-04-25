import os

# Read thesis
with open('C:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system/docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Read appendix content
with open('C:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system/_appendix_content.md', 'r', encoding='utf-8') as f:
    appendix = f.read()

print(f"Before: {len(content)} chars")

# Append appendix
content = content.rstrip() + "\n\n" + appendix + "\n"

# Save
with open('C:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system/docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"After: {len(content)} chars")
print(f"Added: {len(content) - len(content) + len(appendix)} chars")
print("Done!")
