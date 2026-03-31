import re
from pathlib import Path


def normalize_skill_name(name):
    name = name.strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = name.lower()
    name = name.strip('-')
    return name


test_cases = [
    "My Awesome Skill! 123",
    "Another_Skill_With_Spaces",
    "Skill@#$Name!",
    "__SKILL__NAME__",
    "test skill 123",
    "TestSkill",
    "test---skill---",
    "!!!Skill!!!",
    "My Skill (v2.0)",
    "技能测试 123",
]

print("=" * 60)
print("测试命名规范化功能")
print("=" * 60)
print()

for test in test_cases:
    result = normalize_skill_name(test)
    print(f"原始: {test}")
    print(f"结果: {result}")
    print()

print("=" * 60)
print("测试外部Skill扫描")
print("=" * 60)
print()

test_dir = Path("test-external-skills")
if test_dir.exists():
    for item in test_dir.iterdir():
        if item.is_dir():
            print(f"目录: {item.name}")
            
            skill_md = item / "SKILL.md"
            name_from_md = None
            has_md = skill_md.exists()
            
            if has_md:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.startswith('---'):
                        end = content.find('---', 3)
                        if end != -1:
                            frontmatter = content[3:end].strip()
                            for line in frontmatter.split('\n'):
                                if line.startswith('name:'):
                                    name_from_md = line.split(':', 1)[1].strip().strip('"')
            
            if name_from_md:
                normalized = normalize_skill_name(name_from_md)
                print(f"  从SKILL.md读取: {name_from_md}")
            else:
                normalized = normalize_skill_name(item.name)
                print(f"  使用目录名")
            
            print(f"  规范化后: {normalized}")
            print(f"  有SKILL.md: {'是' if has_md else '否'}")
            print()
else:
    print(f"测试目录不存在: {test_dir}")

print("=" * 60)
print("测试完成！")
print("=" * 60)
