$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$docxPath = Join-Path $taskRoot '13_RELATORIO_FINAL/RELATORIO_FINAL_PROJETO_P2.docx'
$pdfPath = Join-Path $taskRoot '13_RELATORIO_FINAL/RELATORIO_FINAL_PROJETO_P2.pdf'
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
$taskDoc = $null
try {
    $taskDoc = $wordApp.Documents.Open($docxPath, $false, $false)
    $taskDoc.Fields.Update() | Out-Null
    $taskDoc.Repaginate()
    foreach ($tocItem in $taskDoc.TablesOfContents) { $tocItem.Update() }
    $taskDoc.Save()
    $taskDoc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('PDF exportado do mesmo DOCX: ' + $pdfPath)
} finally {
    if ($null -ne $taskDoc) { $taskDoc.Close($false) }
    $wordApp.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
}
