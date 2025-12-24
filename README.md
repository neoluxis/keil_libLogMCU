# Keil 函数库模板

此模板提供两个 Keil 项目，分别编写函数库和测试程序。

示例库名为 `libABC`，测试项目为 `libABC_tests`，并有一个多项目工作空间，已经添加了两个项目，可以直接打开。

[参考文档](./doc)

对于本示例函数库来说，虽然函数中没有用到 STM32 相关的固件库，但是仓库中却附带上了，并且 STM32 HAL 库的源码文件并未在库项目中添加，即并不会编译，这样的行为其实是不好的。

通过本模板创建的项目，如果未用到 STM32 固件库，可以直接删掉或忽略相关的源文件和头文件。如果用到了，则需要把源文件添加进项目才能正常编译。

## 使用方法
### Fork 后以模板新建 Repo

1. Fork 此项目到自己的账户
2. 点击右上角 `Use this template`，选择 `Create a new repository`
3. 将仓库克隆到本地，进入文件夹
	```bash
	git clone git@github.com:<username>/keil_library_template.git
	git keil_library_template
	```
4. 运行自动配置脚本
	```text
	# Dry run
	python scripts/project_setup.py
	项目名称(不需要写lib): XXX 对应的项目即为 libXXX
	作者(seekit): Your name
	倒序域名(seekit.dev): Your domain, use your name and dot cc if you don't have one
	E-Mail: Your email, actually no regex matching written
	开源证书(MIT): Usually MIT, GNU or Apache, or any you want

	==================== Git 分支选择 ====================
	[1] main [STM32F10x]
	[2] remotes/origin/main [STM32F10x]

	请选择目标平台编号 (1-2, 默认1): Different branches contain projects for different target platform
	
	# Run!
	python scripts/project_setup.py --run
	项目名称(不需要写lib): PID
	作者(seekit): seekit
	倒序域名(seekit.dev): seekit.dev
	E-Mail: user@email.com
	开源证书(MIT): MIT

	==================== Git 分支选择 ====================
	[1] main [STM32F10x]
	[2] remotes/origin/main [STM32F10x]

	请选择目标平台编号 (1-2, 默认1): 1
	```
	
### 直接利用 Powershell 命令

1. 在某文件夹（例如 E:/）打开 Powershell
2. 如果没有 Python：
	```powershell
	winget install python
	```
3. 运行命令
	```powershell
	& { 
		$env:GITHUB_MIRROR = 'https://git.likangfeng.edu.eu.org/https://github.com'; 
		$m = $env:GITHUB_MIRROR;
		iex ((iwr "$m/neoluxis/keil_library_template/raw/main/scripts/setup.ps1").Content) 
	} 
	```
4. 信息填写如上

## 提交规范

| 前缀 | 含义 |
|:---:|:---:|
| add/feat | 新内容添加 |
| del | 内容删除 |
| fix | 修改 bug |
| revert | 撤销提交，回滚操作 |
| doc | 文档更新 |
| refactor | 代码重构，不影响内部行为、功能的修改 |
| test | 测试用例新增，修改 |
| style | 修改代码风格之类 |
| perf | 在不影响内部行为和功能情况下进行性能优化 |
| chore | 杂项，上述分类未包含的内容，请勿滥用 |

## TODO

### 支持更多目标平台
目前只做了 STM32F10x 的模板，即具有库项目和测试项目的模板，未来可能会制作其他模板。通过不同分支进行区分。

通常很多函数库并不止针对于一种 MCU，而且并不依赖于某种特定芯片的固件库，对于这种函数库可以直接用任意分支开发。

- [x] STM32F10x
- [ ] STM32F40x
- [ ] STM32H72x
- [ ] Other

---

## 备注

1. 通过该模板创建的函数库代码仓库的 README 应描述函数库的内容，用处，使用方法

2. 在 doc 目录中写完整的使用文档并附链接在仓库 README 便于点击查看

3. 创建的仓库名应该与仓库中代码库的名相同或表达相一致的信息，以免产生误解

4. 不允许直接在仓库根目录创建项目，即不允许项目root作为仓库root，避免导致根目录信息过于杂乱

5. 请从一开始就保持仓库整洁，不要把编译后文件、临时文件、临时备忘录等文件添加进来

6. 建议保持源码和二进制两种方式进行分发，并维护好 release、issue、pull request等
