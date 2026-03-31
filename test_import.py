import os
import shutil
from pathlib import Path
import sys

trae_skills_dir = Path.home() / ".trae-cn" / "skills"
source_dir = Path("test-skills")

print("=" * 50)
print("测试 Trae Skill 导入工具")
print("=" * 50)
print()

print(f"Trae Skill目录: {trae_skills_dir}")
print(f"源目录: {source_dir}")
print()

if not trae_skills_dir.exists():
    print(f"警告: Trae Skill目录不存在")
    print(f"创建目录: {trae_skills_dir}")
    trae_skills_dir.mkdir(parents=True, exist_ok=True)
    print()

print("扫描源目录中的Skill...")
found_skills = []
for item in source_dir.iterdir():
    if item.is_dir() and (item / "SKILL.md").exists():
        found_skills.append(item)
        print(f"  ✓ 找到: {item.name}")

print()
print(f"共找到 {len(found_skills)} 个Skill")
print()

print("测试导入功能...")
print()

success_count = 0
for skill_path in found_skills:
    skill_name = skill_path.name
    target_path = trae_skills_dir / skill_name
    
    print(f"处理: {skill_name}")
    
    if target_path.exists():
        print(f"  - 已存在，先删除旧版本")
        shutil.rmtree(target_path)
    
    print(f"  - 正在复制...")
    shutil.copytree(skill_path, target_path)
    
    if (target_path / "SKILL.md").exists():
        print(f"  ✓ 成功导入")
        success_count += 1
    else:
        print(f"  ✗ 导入失败")
    print()

print("=" * 50)
print(f"测试完成！成功导入 {success_count}/{len(found_skills)} 个Skill")
print("=" * 50)
print()
print("验证导入结果...")
print()

for skill_path in found_skills:
    skill_name = skill_path.name
    target_path = trae_skills_dir / skill_name
    
    if target_path.exists():
        print(f"✓ {skill_name} - 已成功导入到 Trae")
        print(f"  位置: {target_path}")
        
        skill_md = target_path / "SKILL.md"
        if skill_md.exists():
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end != -1:
                        frontmatter = content[3:end].strip()
                        print(f"  配置:")
                        for line in frontmatter.split('\n'):
                            print(f"    {line}")
    else:
        print(f"✗ {skill_name} - 导入失败")
    print()

print("测试完成！")
