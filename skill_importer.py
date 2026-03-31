import os
import re
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import json


class SkillImporter:
    def __init__(self, root):
        self.root = root
        self.root.title("Trae Skill 一键导入工具")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)
        
        self.trae_skills_dir = Path.home() / ".trae-cn" / "skills"
        self.source_dir = ""
        self.selected_skills = set()
        self.found_skills = []
        
        self.setup_ui()
        self.check_trae_dir()
    
    @staticmethod
    def normalize_skill_name(name):
        name = name.strip()
        name = re.sub(r'[^\w\s-]', '', name)
        name = re.sub(r'[\s_]+', '-', name)
        name = name.lower()
        name = name.strip('-')
        return name
    
    @staticmethod
    def generate_default_description(dir_name):
        return f"{dir_name} - 自动导入的Skill"
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Microsoft YaHei UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Microsoft YaHei UI', 10))
        style.configure('Accent.TButton', font=('Microsoft YaHei UI', 10), padding=10)
        style.configure('Danger.TButton', font=('Microsoft YaHei UI', 10), padding=10)
        style.configure('Success.TButton', font=('Microsoft YaHei UI', 10), padding=10)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        title_label = ttk.Label(main_frame, text="🔧 Trae Skill 一键导入工具", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        dir_frame = ttk.LabelFrame(main_frame, text="源目录选择", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        dir_frame.columnconfigure(0, weight=1)
        
        self.dir_entry = ttk.Entry(dir_frame, font=('Microsoft YaHei UI', 10))
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_source_dir)
        browse_btn.grid(row=0, column=1)
        
        scan_btn = ttk.Button(dir_frame, text="扫描Skill", command=self.scan_skills)
        scan_btn.grid(row=0, column=2, padx=(10, 0))
        
        self.trae_dir_label = ttk.Label(main_frame, text=f"Trae Skill目录: {self.trae_skills_dir}", style='Subtitle.TLabel', foreground='#666666')
        self.trae_dir_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        list_frame = ttk.LabelFrame(main_frame, text="找到的Skill", padding="10")
        list_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.skill_tree = ttk.Treeview(list_frame, columns=('original_name', 'normalized_name', 'description', 'exists'), show='headings', selectmode='extended')
        self.skill_tree.heading('original_name', text='原始名称')
        self.skill_tree.heading('normalized_name', text='导入名称')
        self.skill_tree.heading('description', text='描述')
        self.skill_tree.heading('exists', text='状态')
        self.skill_tree.column('original_name', width=150)
        self.skill_tree.column('normalized_name', width=150)
        self.skill_tree.column('description', width=250)
        self.skill_tree.column('exists', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.skill_tree.yview)
        self.skill_tree.configure(yscrollcommand=scrollbar.set)
        
        self.skill_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.skill_tree.bind('<<TreeviewSelect>>', self.on_skill_select)
        
        btn_frame = ttk.LabelFrame(main_frame, text="操作", padding="10")
        btn_frame.grid(row=3, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        select_all_btn = ttk.Button(btn_frame, text="全选", command=self.select_all_skills)
        select_all_btn.pack(fill=tk.X, pady=5)
        
        deselect_all_btn = ttk.Button(btn_frame, text="取消全选", command=self.deselect_all_skills)
        deselect_all_btn.pack(fill=tk.X, pady=5)
        
        ttk.Separator(btn_frame).pack(fill=tk.X, pady=10)
        
        import_btn = ttk.Button(btn_frame, text="导入选中的Skill", command=self.import_skills, style='Success.TButton')
        import_btn.pack(fill=tk.X, pady=5)
        
        overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_check = ttk.Checkbutton(btn_frame, text="覆盖已存在的Skill", variable=overwrite_var)
        self.overwrite_check.var = overwrite_var
        self.overwrite_check.pack(anchor=tk.W, pady=5)
        
        ttk.Separator(main_frame).grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        log_frame = ttk.LabelFrame(main_frame, text="日志输出", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Consolas', 9), wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log("欢迎使用 Trae Skill 一键导入工具！")
        self.log("请选择包含Skill的源目录，然后点击'扫描Skill'")
    
    def check_trae_dir(self):
        if not self.trae_skills_dir.exists():
            self.log(f"警告: Trae Skill目录不存在: {self.trae_skills_dir}", "warning")
            messagebox.showwarning("警告", f"Trae Skill目录不存在:\n{self.trae_skills_dir}\n\n请确保Trae已正确安装。")
    
    def browse_source_dir(self):
        directory = filedialog.askdirectory(title="选择包含Skill的目录")
        if directory:
            self.source_dir = directory
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.log(f"已选择源目录: {directory}")
    
    def scan_skills(self):
        if not self.dir_entry.get():
            messagebox.showwarning("警告", "请先选择源目录！")
            return
        
        self.source_dir = Path(self.dir_entry.get())
        if not self.source_dir.exists():
            messagebox.showerror("错误", "源目录不存在！")
            return
        
        self.log(f"正在扫描目录: {self.source_dir}")
        
        for item in self.skill_tree.get_children():
            self.skill_tree.delete(item)
        
        self.found_skills = []
        self.selected_skills = set()
        
        if (self.source_dir / "SKILL.md").exists():
            skill_info = self.parse_skill(self.source_dir)
            if skill_info:
                self.found_skills.append(skill_info)
                self.add_skill_to_tree(skill_info)
        else:
            for item in self.source_dir.iterdir():
                if item.is_dir() and (item / "SKILL.md").exists():
                    skill_info = self.parse_skill(item)
                    if skill_info:
                        self.found_skills.append(skill_info)
                        self.add_skill_to_tree(skill_info)
                elif item.is_file() and item.suffix == '.md' and item.name != "SKILL.md":
                    skill_info = self.parse_single_md_skill(item)
                    if skill_info:
                        self.found_skills.append(skill_info)
                        self.add_skill_to_tree(skill_info)
        
        if not self.found_skills:
            self.log("未找到任何Skill", "warning")
            messagebox.showinfo("提示", "未找到任何Skill！请确保目录结构正确。")
        else:
            self.log(f"找到 {len(self.found_skills)} 个Skill")
    
    def parse_skill(self, skill_path):
        try:
            original_name = skill_path.name
            skill_md = skill_path / "SKILL.md"
            name_from_md = None
            description = ""
            has_skill_md = skill_md.exists()
            
            if has_skill_md:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if content.startswith('---'):
                        end = content.find('---', 3)
                        if end != -1:
                            frontmatter = content[3:end].strip()
                            for line in frontmatter.split('\n'):
                                if line.startswith('name:'):
                                    name_from_md = line.split(':', 1)[1].strip().strip('"')
                                elif line.startswith('description:'):
                                    description = line.split(':', 1)[1].strip().strip('"')
                    
                    if not description:
                        lines = content.split('\n', 20)
                        for line in lines:
                            if line.strip() and not line.startswith('#') and not line.startswith('---'):
                                description = line.strip()[:100]
                                break
            
            if name_from_md:
                normalized_name = self.normalize_skill_name(name_from_md)
            else:
                normalized_name = self.normalize_skill_name(original_name)
            
            if not normalized_name:
                normalized_name = f"skill-{original_name[:10].lower()}"
            
            if not description:
                description = self.generate_default_description(original_name)
            
            exists = (self.trae_skills_dir / normalized_name).exists()
            
            return {
                'path': skill_path,
                'original_name': original_name,
                'normalized_name': normalized_name,
                'name_from_md': name_from_md,
                'description': description,
                'exists': exists,
                'has_skill_md': has_skill_md
            }
        except Exception as e:
            self.log(f"解析Skill {skill_path.name} 失败: {e}", "error")
            return None
    
    def parse_single_md_skill(self, md_file_path):
        try:
            original_name = md_file_path.stem
            description = ""
            
            with open(md_file_path, 'r', encoding='utf-8') as f:
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
                    if not description:
                        for line in lines:
                            if line.strip() and not line.startswith('#') and not line.startswith('---'):
                                description = line.strip()[:100]
                                break
            
            normalized_name = self.normalize_skill_name(original_name)
            if not normalized_name:
                normalized_name = f"skill-{original_name[:10].lower()}"
            
            if not description:
                description = self.generate_default_description(original_name)
            
            exists = (self.trae_skills_dir / normalized_name).exists()
            
            return {
                'path': md_file_path,
                'original_name': original_name,
                'normalized_name': normalized_name,
                'name_from_md': None,
                'description': description,
                'exists': exists,
                'has_skill_md': False,
                'is_single_md': True,
                'md_content': content if 'content' in locals() else ""
            }
        except Exception as e:
            self.log(f"解析Skill {md_file_path.name} 失败: {e}", "error")
            return None
    
    def add_skill_to_tree(self, skill_info):
        status = "已存在" if skill_info['exists'] else "新"
        if skill_info.get('is_single_md'):
            status += " (单文件)"
        elif not skill_info['has_skill_md']:
            status += " (无SKILL.md)"
        
        tags = ('exists',) if skill_info['exists'] else ('new',)
        if not skill_info['has_skill_md'] and not skill_info.get('is_single_md'):
            tags = ('warning',)
        
        self.skill_tree.insert('', tk.END, values=(
            skill_info['original_name'],
            skill_info['normalized_name'],
            skill_info['description'],
            status
        ), tags=tags)
        
        self.skill_tree.tag_configure('exists', foreground='#999999')
        self.skill_tree.tag_configure('new', foreground='#22c55e')
        self.skill_tree.tag_configure('warning', foreground='#f59e0b')
    
    def on_skill_select(self, event):
        selected = self.skill_tree.selection()
        self.selected_skills = set()
        for item in selected:
            idx = self.skill_tree.index(item)
            if idx < len(self.found_skills):
                self.selected_skills.add(idx)
    
    def select_all_skills(self):
        for item in self.skill_tree.get_children():
            self.skill_tree.selection_add(item)
        self.selected_skills = set(range(len(self.found_skills)))
    
    def deselect_all_skills(self):
        for item in self.skill_tree.get_children():
            self.skill_tree.selection_remove(item)
        self.selected_skills = set()
    
    def import_skills(self):
        selected = self.skill_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要导入的Skill！")
            return
        
        overwrite = self.overwrite_check.var.get()
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for item in selected:
            idx = self.skill_tree.index(item)
            if idx >= len(self.found_skills):
                continue
            
            skill_info = self.found_skills[idx]
            target_path = self.trae_skills_dir / skill_info['normalized_name']
            
            try:
                if target_path.exists():
                    if not overwrite:
                        self.log(f"跳过已存在的Skill: {skill_info['normalized_name']}", "warning")
                        skip_count += 1
                        continue
                    else:
                        self.log(f"覆盖已存在的Skill: {skill_info['normalized_name']}")
                        shutil.rmtree(target_path)
                
                self.log(f"正在导入: {skill_info['original_name']} → {skill_info['normalized_name']}")
                
                if skill_info.get('is_single_md'):
                    target_path.mkdir(parents=True, exist_ok=True)
                    self.log(f"  - 从单个MD文件创建Skill")
                    self.create_skill_from_single_md(target_path, skill_info)
                else:
                    shutil.copytree(skill_info['path'], target_path)
                    
                    if not skill_info['has_skill_md']:
                        self.log(f"  - 自动生成 SKILL.md")
                        self.generate_skill_md(target_path, skill_info)
                    
                    if skill_info['name_from_md'] and skill_info['name_from_md'] != skill_info['normalized_name']:
                        self.log(f"  - 更新 SKILL.md 中的 name 字段")
                        self.update_skill_md_name(target_path, skill_info['normalized_name'])
                
                self.log(f"✓ 成功导入: {skill_info['normalized_name']}", "success")
                success_count += 1
                
            except Exception as e:
                self.log(f"✗ 导入失败 {skill_info['original_name']}: {e}", "error")
                error_count += 1
        
        message = f"导入完成！\n\n成功: {success_count}\n跳过: {skip_count}\n失败: {error_count}"
        self.log(message)
        messagebox.showinfo("完成", message)
        
        self.scan_skills()
    
    def generate_skill_md(self, target_path, skill_info):
        skill_md_path = target_path / "SKILL.md"
        content = f"""---
name: {skill_info['normalized_name']}
description: "{skill_info['description']}"
---

# {skill_info['original_name']}

{skill_info['description']}

---

*由 Trae Skill 导入工具自动生成*
"""
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_skill_from_single_md(self, target_path, skill_info):
        skill_md_path = target_path / "SKILL.md"
        original_content = skill_info.get('md_content', '')
        
        if original_content.startswith('---'):
            end = original_content.find('---', 3)
            if end != -1:
                frontmatter = original_content[3:end].strip()
                main_content = original_content[end+3:].strip()
                
                if not any(line.startswith('name:') for line in frontmatter.split('\n')):
                    frontmatter = f'name: {skill_info["normalized_name"]}\n{frontmatter}'
                
                content = f'---\n{frontmatter}\n---\n\n{main_content}'
            else:
                content = f"""---
name: {skill_info['normalized_name']}
description: "{skill_info['description']}"
---

{original_content}
"""
        else:
            content = f"""---
name: {skill_info['normalized_name']}
description: "{skill_info['description']}"
---

{original_content}
"""
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def update_skill_md_name(self, target_path, new_name):
        skill_md_path = target_path / "SKILL.md"
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                end = content.find('---', 3)
                if end != -1:
                    frontmatter = content[3:end].strip()
                    lines = frontmatter.split('\n')
                    new_lines = []
                    name_found = False
                    
                    for line in lines:
                        if line.startswith('name:'):
                            new_lines.append(f'name: {new_name}')
                            name_found = True
                        else:
                            new_lines.append(line)
                    
                    if not name_found:
                        new_lines.insert(0, f'name: {new_name}')
                    
                    new_frontmatter = '\n'.join(new_lines)
                    content = f'---\n{new_frontmatter}\n---{content[end+3:]}'
                    
                    with open(skill_md_path, 'w', encoding='utf-8') as f:
                        f.write(content)
        except Exception as e:
            self.log(f"  - 更新 SKILL.md 失败: {e}", "warning")
    
    def log(self, message, level="info"):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        colors = {
            'info': '#000000',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'error': '#ef4444'
        }
        
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", level)
        self.log_text.see(tk.END)
        
        self.log_text.tag_config("timestamp", foreground='#666666')
        for lvl, color in colors.items():
            self.log_text.tag_config(lvl, foreground=color)


def main():
    root = tk.Tk()
    app = SkillImporter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
