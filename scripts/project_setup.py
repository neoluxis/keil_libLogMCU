#!env python3
import subprocess
import winreg
import sys
import os
import shutil
from pathlib import Path

def find_keil_uv4():
    key = r'Software\Keil\μVision5\Recent Projects'
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key,
        ) as rk:
            value, _ = winreg.QueryValueEx(rk, 'Project 1')
            names = value.split('\\')
            idx = names.index('ARM')
            path = '/'.join(names[:idx])
            path = '/'.join([path, 'UV4', 'UV4.exe'])
            if os.path.exists(path):
                return path
            else: return None
    except FileNotFoundError:
        print("无法找到 Keil 安装")
    except PermissionError:
        print("权限不足（需要管理员）")
    return None

def prepare_environment():
    mirror = os.environ.get("GITHUB_MIRROR", "https://github.com")
    repo_url = f"{mirror.rstrip('/')}/neoluxis/keil_library_template.git"
    template_marker = "libABC.uvmpw"

    if os.path.exists(template_marker):
        print(f"[OK] In repo detected. Ready to setup!")
        return

    print(f"[Info] Not in template repo, cloning...")
    print(f"[URL] {repo_url}")
    
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
        repo_name = "keil_library_template"
        if os.path.exists(repo_name):
            os.chdir(repo_name)
            print(f"[Success] Entering repo: {os.getcwd()}")
        else:
            print("[Error] Cannot find folder, try to clone manually")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"[Error] Cannot clone template from {repo_url}. Check you network or GitHub mirror setup in envvar GITHUB_MIRROR.")
        sys.exit(1)

def simple_replace(path, project, dryrun=True):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
        data = data.replace("libABC", project)
    if not dryrun:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

def gen_versionsch(author, email, lic, target, dryrun=True):
    print(f"\n[Step] Generate versions: Target={target}")
    header = f"""#ifndef __VERSIONS_H
#define __VERSIONS_H

const char* author = "author: {author}";
const char* email = "email: {email}";
const char* license = "license: {lic}";
const char* target_mcu = "target: {target}";
const char* build_date_time = "build: " __DATE__ " " __TIME__ " ";

#endif
"""
    if dryrun:
        print(header)
    else:
        os.makedirs("./libABC/Versions", exist_ok=True)
        with open("./libABC/Versions/versions.h", 'w', encoding='utf-8') as f:
            f.write(header)

def gen_default_c(path, project, domain, dryrun=True):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
        data = data.replace('libABC', project)
        if domain:
            domain_path = "/".join(domain.split('.')[::-1]).lower()
            data = data.replace('dev/seekit', domain_path)
    if not dryrun:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

def gen_default_h(path, project, domain, dryrun=True):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
        data = data.replace('libABC', project)
        data = data.replace('LIBABC', project.upper())
        if domain:
            domain_macro = "_".join(domain.split('.')[::-1]).upper()
            data = data.replace('DEV_SEEKIT', domain_macro)
    if not dryrun:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)

def setup_project(old_domain, old_project, new_domain, new_project, dryrun=True, verbose=False):
    def domain_to_path(domain):
        if not domain: return Path("")
        return Path(*domain.split('.')[::-1])

    old_root, new_root = Path(old_project), Path(new_project)
    old_test_root, new_test_root = Path(f"{old_project}_tests"), Path(f"{new_project}_tests")
    old_dom_path = domain_to_path(old_domain)
    new_dom_path = domain_to_path(new_domain if new_domain else old_domain)

    print(f"\n{' [Rehearsal] ' if dryrun else ' [Start migrating...] ':=^60}")

    old_pw = Path(f"{old_project}.uvmpw")
    new_pw = Path(f"{new_project}.uvmpw")
    if old_pw.exists():
        if dryrun: print(f"[Plan] Rename werkspazio: {old_pw} -> {new_pw}")
        else: os.rename(old_pw, new_pw)

    roots = [(old_root, new_root), (old_test_root, new_test_root)]
    for o_r, n_r in roots:
        if o_r.exists() and not n_r.exists():
            if dryrun: print(f"[Plan] Rename dir: {o_r} -> {n_r}")
            else: os.rename(o_r, n_r)

    base_lib = new_root if not dryrun else old_root
    base_test = new_test_root if not dryrun else old_test_root

    tasks = [
        (base_lib / "Library" / "inc" / old_dom_path / old_project / f"{old_project}.h", 
         new_root / "Library" / "inc" / new_dom_path / new_project / f"{new_project}.h"),
        (base_lib / "Library" / "src" / f"{old_project}.c", 
         new_root / "Library" / "src" / f"{new_project}.c"),
        (base_lib / "MDK-ARM" / f"{old_project}.uvprojx", 
         new_root / "MDK-ARM" / f"{new_project}.uvprojx"),
        (base_test / "MDK-ARM" / f"{old_project}_tests.uvprojx", 
         new_test_root / "MDK-ARM" / f"{new_project}_tests.uvprojx")
    ]

    for src, dst in tasks:
        if src.exists():
            if dryrun: print(f"[Plan] Move files: {src} -> {dst}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                if verbose: print(f"[Done] Moved: {src.name}")

    if not dryrun:
        clean_target = new_root / "Library" / "inc" / old_dom_path / old_project
        curr = clean_target
        while curr != (new_root / "Library" / "inc"):
            if curr.exists() and not os.listdir(curr):
                curr.rmdir()
                curr = curr.parent
            else: break


def get_git_branches():
    try:
        result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True, check=True)
        lines = result.stdout.split('\n')
        branches = []
        for line in lines:
            line = line.strip()
            if not line or '->' in line: continue
            clean_br = line.replace('* ', '').strip()
            branches.append(clean_br)
        return branches
    except Exception as e:
        print(f"\n[Warn] Failed to fetch git branches: {e}")
        return []

def main(dryrun=True):
    prepare_environment()
    
    branch2target = {"main": "STM32F10x"}
    
    project_input = input("项目名称(不需要写lib): ")
    project = "lib" + project_input
    author = input("作者(seekit): ")
    domain = input("域名(seekit.dev): ")
    email = input("E-Mail: ")
    lic = input("开源证书(MIT): ")

    branches = get_git_branches()
    target_mcu = "Unknown"
    
    if branches:
        print("\n" + "="*20 + " Git 分支选择 " + "="*20)
        display_list = []
        for br in branches:
            desc = ""
            for k, v in branch2target.items():
                if k in br: desc = f" [{v}]"
            display_list.append(f"{br}{desc}")
        
        for idx, val in enumerate(display_list, 1):
            print(f"[{idx}] {val}")
        
        try:
            choice_str = input(f"\n请选择目标平台编号 (1-{len(branches)}, 默认1): ")
            choice = int(choice_str) if choice_str else 1
            selected_branch = branches[choice - 1]
            
            if selected_branch.startswith('remotes/'):
                clean_br_name = selected_branch.split('/')[-1]
                subprocess.run(['git', 'checkout', '-b', clean_br_name, '--track', selected_branch])
                final_branch = clean_br_name
            else:
                subprocess.run(['git', 'checkout', selected_branch])
                final_branch = selected_branch
            
            target_mcu = final_branch
            for k, v in branch2target.items():
                if k in final_branch: target_mcu = v
        except Exception as e:
            print(f"Failed to switch branch: {e}")
    else:
        print("\n[Hint] No branch found in folder. Branch switch skipped.")

    print(f"\n{' [Updating file content] ':=^60}")
    simple_replace("./libABC.uvmpw", project, dryrun)
    
    simple_replace("./scripts/lib_mv2test.bat", project, dryrun)
    simple_replace("./libABC/MDK-ARM/libABC.uvprojx", project, dryrun)
    simple_replace("./libABC_tests/MDK-ARM/libABC_tests.uvprojx", project, dryrun)
    
    gen_default_c("./libABC_tests/Core/Src/main.c", project, domain, dryrun)
    gen_versionsch(author, email, lic, target_mcu, dryrun)
    gen_default_c("./libABC/Library/src/libABC.c", project, domain, dryrun)
    gen_default_c("./libABC/Library/src/example_oop.c", project, domain, dryrun)
    gen_default_h("./libABC/Library/inc/dev/seekit/libABC/libABC.h", project, domain, dryrun)
    gen_default_h("./libABC/Library/inc/dev/seekit/libABC/example_oop.h", project, domain, dryrun)

    setup_project("seekit.dev", "libABC", domain, project, dryrun, verbose=True)
    return project

if __name__ == "__main__":
    is_dryrun = '--run' not in sys.argv
    try:
        project = main(dryrun=is_dryrun)
        if is_dryrun:
            print(f"\n{' Rehearsal Ends. Add cmdline argument --run to run. ':=^60}")
        else:
            opener = input("打开工作空间？(Y/n) ").lower()
            if opener != 'y':
                pass
            keil = find_keil_uv4()
            if not keil:
                print("没有找到 Keil，请手动打开")
            else:
                subprocess.Popen([keil, f'{project}.uvmpw'])
            
    except KeyboardInterrupt:
        print("\n\n[Quit] User interrupted")
        sys.exit(0)