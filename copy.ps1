# ファイルパスの定義
$debugDllPath = ".\target\debug\primitive_ffi.dll"
$releaseDllPath = ".\target\release\primitive_ffi.dll"
$artifactPath = ".\artifacts\primitive_ffi.dll"

if (!(Test-Path $debugDllPath) -and (Test-Path $releaseDllPath))
{
    Copy-Item $releaseDllPath -Destination $artifactPath -Force
    Write-Output "Copied $releaseDllPath to $artifactPath"
}

if ((Test-Path $debugDllPath) -and !(Test-Path $releaseDllPath))
{
    Copy-Item $releaseDllPath -Destination $artifactPath -Force
    Write-Output "Copied $releaseDllPath to $artifactPath"
}


# ファイルの存在確認
if ((Test-Path $debugDllPath) -and (Test-Path $releaseDllPath))
{
    # ファイル情報の取得
    $debugDllInfo = Get-Item $debugDllPath
    $releaseDllInfo = Get-Item $releaseDllPath

    # 作成日時の比較
    if ($debugDllInfo.CreationTime -gt $releaseDllInfo.CreationTime)
    {
        Copy-Item $debugDllPath -Destination $artifactPath -Force
        Write-Output "Copied $debugDllPath to $artifactPath"
    }
    elseif ($releaseDllInfo.CreationTime -gt $debugDllInfo.CreationTime)
    {
        Copy-Item $releaseDllPath -Destination $artifactPath -Force
        Write-Output "Copied $releaseDllPath to $artifactPath"
    }
    else
    {
        Write-Output "Both files have the same creation time. No copy performed."
    }
}
else
{
    Write-Output "One or both of the files do not exist. Please check the file paths."
}