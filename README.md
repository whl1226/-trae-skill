# Trae Skill 一键导入工具

一个简单易用的图形界面工具，用于批量导入外部Skill到Trae IDE。

## 功能特性

- 📁 可视化选择源目录
- 🔍 自动扫描目录中的Skill
- ✅ 支持多选和全选
- ⚠️ 智能检测已存在的Skill
- 🔄 可选覆盖已存在的Skill
- 📝 实时日志输出
- 🎨 简洁美观的界面
- 🔧 **智能命名适配** - 自动规范化外部Skill的名称
- 📄 **自动生成SKILL.md** - 为没有配置文件的Skill自动创建
- 🔄 **同步名称更新** - 自动更新SKILL.md中的name字段

## 使用方法

### 1. 启动程序

双击 `启动.bat` 文件，或在命令行中运行：

```bash
python skill_importer.py
```

### 2. 选择源目录

点击"浏览..."按钮，选择包含Skill的目录（例如桌面的 `TRAE-Skills-main` 文件夹）。

### 3. 扫描Skill

点击"扫描Skill"按钮，程序会自动扫描目录中的所有Skill。

### 4. 查看和选择Skill

- **原始名称**：显示外部Skill的原始文件夹名
- **导入名称**：显示规范化后的Trae兼容名称
- **描述**：Skill的描述信息
- **状态**：显示是否已存在、是否有SKILL.md

点击列表中的Skill进行选择，支持多选和全选。

### 5. 导入Skill

- 如果需要覆盖已存在的Skill，勾选"覆盖已存在的Skill"
- 点击"导入选中的Skill"按钮
- 等待导入完成，查看日志输出

## 智能命名适配

工具会自动处理外部Skill的命名，使其符合Trae的规范：

### 命名规范化规则

1. **优先使用SKILL.md中的name字段**
   - 如果SKILL.md中定义了`name:`，会优先使用这个名称
   - 然后对这个名称进行规范化处理

2. **如果没有name字段，使用目录名**
   - 去除特殊字符（!@#$%^&*等）
   - 将空格和下划线转换为连字符（-）
   - 转换为小写
   - 去除首尾的连字符

### 示例转换

| 原始名称 | 规范化后 |
|---------|---------|
| `My Awesome Skill! 123` | `my-awesome-skill-123` |
| `Another_Skill_With_Spaces` | `another-skill-with-spaces` |
| `Skill@#$Name!` | `skill-name` |
| `__SKILL__NAME__` | `skill-name` |

## 自动生成SKILL.md

如果导入的Skill没有SKILL.md文件，工具会自动创建一个：

```markdown
---
name: normalized-skill-name
description: "Original Name - 自动导入的Skill"
---

# Original Name

Original Name - 自动导入的Skill

---

*由 Trae Skill 导入工具自动生成*
```

## 同步名称更新

如果SKILL.md中的name字段与规范化后的名称不一致，工具会自动更新SKILL.md中的name字段，使其保持一致。

## Skill目录结构要求

工具支持三种目录结构：

### 结构1：单个Skill目录
```
your-skill/
└── SKILL.md
```

### 结构2：包含多个Skill的目录
```
TRAE-Skills-main/
├── skill-1/
│   └── SKILL.md
├── skill-2/
│   └── SKILL.md
└── skill-3/
    └── SKILL.md
```

### 结构3：单个MD文件格式（新增）
```
documentation/
├── API_Documentation_Best_Practices.md
├── Code_Comments_Best_Practices.md
└── Writing_Effective_README.md
```

**说明：** 工具会自动识别单个MD文件，并将其转换为Trae兼容的Skill格式：
- 从文件名生成Skill名称（去除.md后缀）
- 自动创建包含SKILL.md的文件夹
- 如果MD文件有frontmatter，会保留并添加name字段
- 如果没有frontmatter，会自动生成完整的配置

## 系统要求

- Windows 操作系统
- Python 3.6 或更高版本（使用Tkinter，Python默认已包含）

## Trae Skill目录

工具默认会将Skill导入到：
```
C:\Users\你的用户名\.trae-cn\skills\
```

## 常见问题

**Q: 提示"Trae Skill目录不存在"怎么办？**
A: 请确保你已经安装并启动过Trae IDE。

**Q: 导入的Skill没有显示在Trae中？**
A: 请重启Trae IDE，新导入的Skill会在重启后生效。

**Q: 可以导入单个Skill吗？**
A: 可以！直接选择该Skill所在的目录即可。

## 技术说明

- 使用Python Tkinter构建GUI界面
- 自动解析SKILL.md文件中的frontmatter获取name和description
- 使用shutil进行目录复制
- 支持中文文件名和路径

## 许可证

本工具仅供学习和个人使用。
