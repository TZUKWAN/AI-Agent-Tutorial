$docx = 'D:\AISOP\AI-Agent-Tutorial\05_Word\AI-Agent零基础工作方法教程.docx'
$pdf = 'D:\AISOP\AI-Agent-Tutorial\05_Word\preview.pdf'

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docx, $false, $true)

# Update all fields (including TOC)
$doc.Fields.Update() | Out-Null
# Also update TOC specifically
foreach ($toc in $doc.TablesOfContents) {
    $toc.Update()
}

# Export to PDF
$doc.ExportAsFixedFormat($pdf, 17)
$pageCount = $doc.ComputeStatistics(2)  # wdStatisticPages = 2
Write-Host "Pages: $pageCount"

$doc.Close($false)
$word.Quit()

if (Test-Path $pdf) {
    $f = Get-Item $pdf
    Write-Host "PDF: $([math]::Round($f.Length/1KB,0)) KB"
}
