$root = (Get-Location).Path
$out = Join-Path $root "project_source_report.txt"

$files = Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch '[\\/](venv|\.venv|\.git|__pycache__|node_modules|migrations|\.idea)[\\/]' -and
        (
            $_.Name -in @("urls.py", "views.py", "models.py", "settings.py", "manage.py") -or
            (
                $_.Extension -in @(".html", ".css", ".js") -and
                $_.FullName -match '[\\/](templates|static)[\\/]'
            )
        )
    } |
    Sort-Object FullName

$writer = [System.IO.StreamWriter]::new($out, $false, [System.Text.UTF8Encoding]::new($false))
try {
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($root.Length).TrimStart('\')
        $writer.WriteLine("")
        $writer.WriteLine(("=" * 60))
        $writer.WriteLine("FILE: " + $relative)
        $writer.WriteLine(("=" * 60))
        $writer.WriteLine((Get-Content -LiteralPath $file.FullName -Raw))
    }
}
finally {
    $writer.Dispose()
}
Write-Host "Report saved:" $out
Write-Host "Files collected:" $files.Count
