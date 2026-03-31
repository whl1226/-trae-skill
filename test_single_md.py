import re
from pathlib import Path


def normalize_skill_name(name):
    name = name.strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = name.lower()
    name = name.strip('-')
    return name


test_dir = Path(r"C:\Users\白鹿与松树\Desktop\TRAE-Skills-main\documentation")

print("=" * 60)
print("测试单个MD文件格式识别")
print("=" * 60)
print()

if test_dir.exists():
    print(f"扫描目录: {test_dir}")
    print()
    
    found_files = []
    for item in test_dir.iterdir():
        if item.is_file() and item.suffix == '.md' and item.name != "SKILL.md":
            found_files.append(item)
            
            original_name = item.stem
            normalized_name = normalize_skill_name(original_name)
            
            description = ""
            with open(item, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end != -1:
                        frontmatter = content[3:end].strip()
                        for line in frontmatter.split('\n'):
                            if line.startswith('description:'):
                                description = line.split(':', 1)[1].strip().strip('"')
                
                if not description:
                    lines = content.split('\n', 20)
                    for line in lines:
                        if line.startswith('#'):
                            description = line.lstrip('#').strip()[:100]
                            break
            
            print(f"文件: {item.name}")
            print(f"  原始名称: {original_name}")
            print(f"  规范化名称: {normalized_name}")
            print(f"  描述: {description}")
            print()
    
    print("=" * 60)
    print(f"找到 {len(found_files)} 个单个MD文件格式的Skill")
    print("=" * 60)
else:
    print(f"目录不存在: {test_dir}")
