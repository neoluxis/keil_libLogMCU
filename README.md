# Keil 函数库模板

此模板提供两个 Keil 项目，分别编写函数库和测试程序。

示例库名为 `libABC`，测试项目为 `libABC_tests`，并有一个多项目工作空间，已经添加了两个项目，可以直接打开。

下面介绍一下使用方法

## Fork 后以模板新建 Repo

1. Fork 此项目到自己的账户
2. 点击右上角 `Use this template`，选择 `Create a new repository`
3. 将仓库克隆到本地，进入文件夹
	```bash
	git clone git@github.com:<username>/keil_library_template.git
	git keil_library_template
	```
4. 运行自动配置脚本
	```bash
	# Dry run
	python ..\project_setup.py
	项目名称(不需要写lib): libXXX
	作者(seekit): Your name
	倒序域名(seekit.dev): Your domain. Use your name dot cc if without one.
	E-Mail: Your email
	开源证书(MIT): Usually MIT, GNU or Apache, or any you want

	==================== Git 分支选择 ====================
	[1] main [STM32F10x]
	[2] remotes/origin/main [STM32F10x]

	请选择目标平台编号 (1-2, 默认1): Different branches contain projects for different target platform
	
	# Run!
	python ..\project_setup.py
	项目名称(不需要写lib): libPID
	作者(seekit): neolux
	倒序域名(seekit.dev): neolux.cc
	E-Mail: user@email.com
	开源证书(MIT): MIT

	==================== Git 分支选择 ====================
	[1] main [STM32F10x]
	[2] remotes/origin/main [STM32F10x]

	请选择目标平台编号 (1-2, 默认1): 1
	```
	
## 直接利用 Powershell 命令

1. 在某文件夹（例如 E:/）打开 Powershell
2. 如果没有 Python：
	```powershell
	winget install python
	```
3. 运行命令
	```Powershell
	& { 
		$env:GITHUB_MIRROR = 'https://git.likangfeng.edu.eu.org/https://github.com'; 
		$m = $env:GITHUB_MIRROR;
		iex ((iwr "$m/neoluxis/keil_library_template/raw/main/scripts/setup.ps1").Content) 
	} 
	```
4. 设置参数即可

## TODO

- [x] STM32F10x
- [ ] STM32F40x
- [ ] Other

