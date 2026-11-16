param([switch]$DownloadTools)
$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$tools = Join-Path $repo '.parispcfix-tools'
$flutter = Join-Path $tools 'flutter/bin/flutter.bat'
$vcpkg = Join-Path $tools 'vcpkg/vcpkg.exe'
function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Program exited with code $LASTEXITCODE" }
}

if ($DownloadTools) {
    New-Item -ItemType Directory -Path $tools -Force | Out-Null
    if (-not (Test-Path -LiteralPath $flutter)) {
        Write-Host 'Downloading Flutter 3.24.5 from the official release archive...'
        $manifest = Invoke-RestMethod 'https://storage.googleapis.com/flutter_infra_release/releases/releases_windows.json'
        $release = @($manifest.releases | Where-Object { $_.version -eq '3.24.5' -and $_.channel -eq 'stable' })[0]
        if (-not $release -or -not $release.sha256 -or -not $release.archive) { throw 'Pinned Flutter release not found.' }
        $archive = Join-Path $tools 'flutter-3.24.5.zip'
        Invoke-WebRequest ($manifest.base_url + '/' + $release.archive) -OutFile $archive
        if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash -ne $release.sha256) { throw 'Flutter SHA256 mismatch.' }
        Expand-Archive -LiteralPath $archive -DestinationPath $tools
    }
    if (-not (Test-Path -LiteralPath (Join-Path $tools 'vcpkg/.git'))) {
        Invoke-Checked 'git' @('clone', 'https://github.com/microsoft/vcpkg.git', (Join-Path $tools 'vcpkg'))
    }
    Invoke-Checked 'git' @('-C', (Join-Path $tools 'vcpkg'), 'checkout', '9e593bb18ea69cc5095e012465dcd675a822ed0d')
    if (-not (Test-Path -LiteralPath $vcpkg)) {
        Invoke-Checked (Join-Path $tools 'vcpkg/bootstrap-vcpkg.bat') @('-disableMetrics')
    }
}

$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
$visualStudio = if (Test-Path -LiteralPath $vswhere) {
    & $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
} else { '' }
$clang = if ($visualStudio) { Join-Path $visualStudio 'VC/Tools/Llvm/x64/bin/libclang.dll' } else { '' }
$bridge = @('src/bridge_generated.rs', 'src/bridge_generated.io.rs', 'flutter/lib/generated_bridge.dart', 'flutter/lib/generated_bridge.freezed.dart')
$bridgeMissing = @($bridge | Where-Object { -not (Test-Path -LiteralPath (Join-Path $repo $_)) })
Write-Host "Repository: $repo"
Write-Host "C++ build tools: $visualStudio"
Write-Host "Flutter: $(Test-Path -LiteralPath $flutter)"
Write-Host "vcpkg: $(Test-Path -LiteralPath $vcpkg)"
Write-Host "libclang: $($clang -and (Test-Path -LiteralPath $clang))"
Write-Host "Generated bridge ready: $($bridgeMissing.Count -eq 0)"
if ($bridgeMissing.Count) {
    Write-Host 'The generated bridge must come from the repository CI; local code generation is not run.'
    Write-Host 'Workflow: .github/workflows/parispcfix-windows.yml'
}
Write-Host 'This command prepares tools only. It does not install a client, enable access, or change autostart.'
