# scripts/setup.ps1
$mirror = $env:GITHUB_MIRROR
if (-not $mirror) { $mirror = "https://github.com" }
$mirror = $mirror.TrimEnd('/')

$pyUrl = "$mirror/neoluxis/keil_library_template/raw/main/scripts/project_setup.py"
$tempFile = "$env:TEMP\tmp_setup_$(Get-Random).py"

Write-Host "[*] Mirror: $mirror" -ForegroundColor Cyan
try {
    # 下载为临时文件
    Invoke-WebRequest -Uri $pyUrl -OutFile $tempFile -UseBasicParsing
    
    # 正常运行文件，参数透传
    python $tempFile --run
    
    # 运行结束后删除临时文件
    Remove-Item $tempFile -ErrorAction SilentlyContinue
}
catch {
    Write-Error "下载或执行失败。"
    if (Test-Path $tempFile) { Remove-Item $tempFile }
}