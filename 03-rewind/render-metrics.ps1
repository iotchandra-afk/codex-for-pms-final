# Render two metric charts using the Windows .NET charting library.
# Inputs and outputs stay within this course module.
Add-Type -AssemblyName System.Windows.Forms.DataVisualization
Add-Type -AssemblyName System.Drawing

$moduleRoot = $PSScriptRoot
$weeklyRows = Get-Content -LiteralPath (Join-Path $moduleRoot 'evidence/weekly-metrics.json') -Raw | ConvertFrom-Json
$responderRows = Get-Content -LiteralPath (Join-Path $moduleRoot 'evidence/responder-weeks.json') -Raw | ConvertFrom-Json
$cohortNames = @('Farlight', 'Vesper', 'The Undertow', 'Meteor Mite')
$navy = [System.Drawing.ColorTranslator]::FromHtml('#102A43')
$blue = [System.Drawing.ColorTranslator]::FromHtml('#1678B5')
$amber = [System.Drawing.ColorTranslator]::FromHtml('#BC6C00')
$grid = [System.Drawing.ColorTranslator]::FromHtml('#DEE5EB')
$chart = New-Object System.Windows.Forms.DataVisualization.Charting.Chart
$chart.Width = 1600
$chart.Height = 1120
$chart.BackColor = [System.Drawing.Color]::White
$chart.AntiAliasing = 'All'
$chart.TextAntiAliasingQuality = 'High'
$chart.Font = New-Object System.Drawing.Font('Segoe UI', 12)

try {
    $title = $chart.Titles.Add('Headline recovery masks lost access')
    $title.Font = New-Object System.Drawing.Font('Segoe UI', 27, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = $navy
    $subtitle = $chart.Titles.Add('ROOK DISPATCH  |  29 June - 6 September 2026  |  All 16 responders included')
    $subtitle.Font = New-Object System.Drawing.Font('Segoe UI', 13)
    $subtitle.ForeColor = $navy

    foreach ($areaName in @('Acceptance', 'Exposure')) {
        $area = New-Object System.Windows.Forms.DataVisualization.Charting.ChartArea($areaName)
        $area.BackColor = [System.Drawing.Color]::White
        $area.AxisX.Minimum = 0
        $area.AxisX.Maximum = 9
        $area.AxisX.Interval = 1
        $area.AxisX.MajorGrid.Enabled = $false
        $area.AxisX.LabelStyle.Font = New-Object System.Drawing.Font('Segoe UI', 11)
        $area.AxisY.Minimum = 0
        $area.AxisY.MajorGrid.LineColor = $grid
        $area.AxisY.LabelStyle.Font = New-Object System.Drawing.Font('Segoe UI', 11)
        $area.AxisY.LabelStyle.Format = '0'
        $area.AxisY.TitleFont = New-Object System.Drawing.Font('Segoe UI', 12)
        $area.AxisX.TitleFont = New-Object System.Drawing.Font('Segoe UI', 12)
        $area.AxisX.LineColor = $grid
        $area.AxisY.LineColor = $grid
        $strip = New-Object System.Windows.Forms.DataVisualization.Charting.StripLine
        $strip.IntervalOffset = 5.5
        $strip.StripWidth = 1
        $strip.BackColor = [System.Drawing.Color]::FromArgb(35, $amber)
        $strip.Text = 'Release week'
        $strip.ForeColor = $amber
        $strip.Font = New-Object System.Drawing.Font('Segoe UI', 10)
        $area.AxisX.StripLines.Add($strip)
        $chart.ChartAreas.Add($area)
    }
    $chart.ChartAreas['Acceptance'].Position = New-Object System.Windows.Forms.DataVisualization.Charting.ElementPosition(5, 13, 90, 34)
    $chart.ChartAreas['Acceptance'].AxisY.Maximum = 100
    $chart.ChartAreas['Acceptance'].AxisY.Interval = 20
    $chart.ChartAreas['Acceptance'].AxisY.Title = 'Taken / all pings (%)'
    $chart.ChartAreas['Acceptance'].AxisX.Title = 'Week starting (Monday)'
    $chart.ChartAreas['Exposure'].Position = New-Object System.Windows.Forms.DataVisualization.Charting.ElementPosition(5, 55, 90, 31)
    $chart.ChartAreas['Exposure'].AxisY.Maximum = 60
    $chart.ChartAreas['Exposure'].AxisY.Interval = 10
    $chart.ChartAreas['Exposure'].AxisY.Title = 'Offers to four responders (combined)'
    $chart.ChartAreas['Exposure'].AxisX.Title = 'Week starting (Monday)'

    $acceptance = $chart.Series.Add('Weekly acceptance')
    $acceptance.ChartArea = 'Acceptance'
    $acceptance.ChartType = 'Line'
    $acceptance.Color = $blue
    $acceptance.BorderWidth = 4
    $acceptance.MarkerStyle = 'Circle'
    $acceptance.MarkerSize = 9

    $baseline = $chart.Series.Add('Six-week baseline: 76.8%')
    $baseline.ChartArea = 'Acceptance'
    $baseline.ChartType = 'Line'
    $baseline.Color = $navy
    $baseline.BorderWidth = 2
    $baseline.BorderDashStyle = 'Dash'

    $exposure = $chart.Series.Add('Four responders: offers per week')
    $exposure.ChartArea = 'Exposure'
    $exposure.ChartType = 'Line'
    $exposure.Color = $amber
    $exposure.BorderWidth = 4
    $exposure.MarkerStyle = 'Circle'
    $exposure.MarkerSize = 9

    for ($rowIndex = 0; $rowIndex -lt $weeklyRows.Count; $rowIndex++) {
        $weekRow = $weeklyRows[$rowIndex]
        $dateLabel = [datetime]::ParseExact($weekRow.week_start, 'yyyy-MM-dd', [System.Globalization.CultureInfo]::InvariantCulture).ToString('d MMM', [System.Globalization.CultureInfo]::InvariantCulture)
        $rate = 100.0 * [double]$weekRow.taken / [double]$weekRow.pings
        $pointIndex = $acceptance.Points.AddXY($rowIndex, $rate)
        $acceptance.Points[$pointIndex].AxisLabel = $dateLabel
        $acceptance.Points[$pointIndex].Label = $rate.ToString('0.0', [System.Globalization.CultureInfo]::InvariantCulture) + '%'
        $acceptance.Points[$pointIndex].Font = New-Object System.Drawing.Font('Segoe UI', 11)
        [void]$baseline.Points.AddXY($rowIndex, 100.0 * 794 / 1034)
        $cohortOfferSum = 0
        foreach ($responderRow in $responderRows) {
            if ($responderRow.week_start -eq $weekRow.week_start -and $cohortNames -contains $responderRow.responder) {
                $cohortOfferSum += [int]$responderRow.pings
            }
        }
        $cohortPoint = $exposure.Points.AddXY($rowIndex, $cohortOfferSum)
        $exposure.Points[$cohortPoint].AxisLabel = $dateLabel
        $exposure.Points[$cohortPoint].Label = $cohortOfferSum.ToString()
        $exposure.Points[$cohortPoint].Font = New-Object System.Drawing.Font('Segoe UI', 11)
    }

    $legend = New-Object System.Windows.Forms.DataVisualization.Charting.Legend
    $legend.Docking = 'Bottom'
    $legend.Font = New-Object System.Drawing.Font('Segoe UI', 11)
    $legend.Position = New-Object System.Windows.Forms.DataVisualization.Charting.ElementPosition(8, 48, 84, 4)
    $legend.LegendStyle = 'Row'
    $legend.IsTextAutoFit = $false
    $chart.Legends.Add($legend)
    $footer = $chart.Titles.Add('Four: Farlight, Vesper, The Undertow, Meteor Mite. Zero-offer weeks retained. Eligibility is unobserved.')
    $footer.Docking = 'Bottom'
    $footer.Font = New-Object System.Drawing.Font('Segoe UI', 11)
    $footer.ForeColor = $navy
    $source = $chart.Titles.Add('Fictional course data: 1,696 pings, 1,319 incidents. Release week contains both pre- and post-12 August records.')
    $source.Docking = 'Bottom'
    $source.Font = New-Object System.Drawing.Font('Segoe UI', 10)
    $source.ForeColor = $navy

    $outputPath = Join-Path $moduleRoot 'metrics-trends.png'
    $chart.SaveImage($outputPath, [System.Windows.Forms.DataVisualization.Charting.ChartImageFormat]::Png)
    Get-Item -LiteralPath $outputPath | Select-Object FullName, Length
} finally {
    $chart.Dispose()
}

