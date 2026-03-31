from pathlib import Path
import yaml

skills_dir = Path(r"C:\Users\白鹿与松树\.trae-cn\skills")

def test_skill_format(skill_dir):
    print(f"\n🔍 测试 Skill: {skill_dir.name}")
    print("=" * 50)
    
    # 检查 SKILL.md 文件是否存在
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print("❌ SKILL.md 文件不存在")
        return False
    
    print("✅ SKILL.md 文件存在")
    
    # 读取 SKILL.md 文件
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 frontmatter
        if not content.startswith('---'):
            print("❌ 缺少 frontmatter")
            return False
        
        end = content.find('---', 3)
        if end == -1:
            print("❌ frontmatter 格式不正确")
            return False
        
        frontmatter = content[3:end].strip()
        
        # 解析 frontmatter
        try:
            frontmatter_data = yaml.safe_load(frontmatter)
            if not isinstance(frontmatter_data, dict):
                print("❌ frontmatter 格式不正确")
                return False
            
            # 检查必要字段
            if 'name' not in frontmatter_data:
                print("❌ 缺少 name 字段")
                return False
            if 'description' not in frontmatter_data:
                print("❌ 缺少 description 字段")
                return False
            
            print(f"✅ 名称: {frontmatter_data['name']}")
            print(f"✅ 描述: {frontmatter_data['description']}")
            
        except Exception as e:
            print(f"❌ 解析 frontmatter 失败: {e}")
            return False
        
        # 检查内容
        main_content = content[end+3:].strip()
        if not main_content:
            print("❌ 缺少内容")
            return False
        
        print("✅ 内容存在")
        print("✅ 格式正确！")
        return True
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

# 测试所有导入的文档类 skill
documentation_skills = [
    "api-documentation-best-practices",
    "architectural-decision-records-adr",
    "changelog-maintenance",
    "code-comments-best-practices",
    "contributing-guidelines-contributing",
    "project-onboarding-guide",
    "user-manual-creation",
    "writing-effective-readme"
]

print("🧪 测试新导入的文档类 Skill")
print("=" * 60)

passed = 0
failed = 0

for skill_name in documentation_skills:
    skill_path = skills_dir / skill_name
    if skill_path.exists():
        if test_skill_format(skill_path):
            passed += 1
        else:
            failed += 1
    else:
        print(f"❌ Skill 目录不存在: {skill_name}")
        failed += 1

print("\n" + "=" * 60)
print("测试结果:")
print(f"✅ 通过: {passed}")
print(f"❌ 失败: {failed}")
print(f"📊 成功率: {passed / (passed + failed) * 100:.1f}%")
print("=" * 60)

if failed == 0:
    print("🎉 所有文档类 Skill 测试通过！")
else:
    print("⚠️  部分 Skill 测试失败，请检查")
