import os
import subprocess

def build_word():
    md_file = "docs/博士论文_最终定稿版_v10.md"
    docx_file = "docs/博士论文_最终完整版_v16.docx"
    
    # Check if pandoc is available
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
    except Exception as e:
        print(f"Pandoc not found or error: {e}")
        return False
        
    print(f"Building {docx_file} from {md_file}...")
    
    # Run pandoc
    cmd = [
        "pandoc",
        md_file,
        "-o", docx_file,
        "--from=markdown",
        "--to=docx",
        "--highlight-style=tango",
        "--toc",
        "--toc-depth=3"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Success! Created {docx_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building Word document: {e.stderr}")
        return False

if __name__ == "__main__":
    build_word()
