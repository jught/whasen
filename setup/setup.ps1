Add-Type -AssemblyName PresentationFramework
Add-Type -AssemblyName WindowsBase
Add-Type -AssemblyName System.Drawing
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Crear ventana principal
$Window = New-Object Windows.Window
$Window.Title = 'WhaSEN'
$Window.Width = 400
$Window.Height = 300
$Window.WindowStartupLocation = 'CenterScreen'

# Crear Grid para organizar los controles
$Grid = New-Object Windows.Controls.Grid
$Window.Content = $Grid

# Definir cuatro filas en el Grid
1..4 | ForEach-Object {
    $Row = New-Object Windows.Controls.RowDefinition
    $Grid.RowDefinitions.Add($Row)
}

# Función para cargar íconos desde shell32.dll
function Get-SystemIcon {
    param([int]$index)
    $iconPath = "$env:SystemRoot\System32\shell32.dll"
    $icon = [System.Drawing.Icon]::ExtractAssociatedIcon($iconPath)
    $memoryStream = New-Object System.IO.MemoryStream
    $icon.ToBitmap().Save($memoryStream, [System.Drawing.Imaging.ImageFormat]::Png)
    $memoryStream.Position = 0

    $bitmap = New-Object System.Windows.Media.Imaging.BitmapImage
    $bitmap.BeginInit()
    $bitmap.StreamSource = $memoryStream
    $bitmap.CacheOption = [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad
    $bitmap.EndInit()
    return $bitmap
}

### BOTÓN "ABRIR FICHERO"
$ButtonOpenFile = New-Object Windows.Controls.Button
$ButtonOpenFile.Content = "Abrir Fichero"
$ButtonOpenFile.Width = 150
$ButtonOpenFile.Height = 40
$ButtonOpenFile.Margin = '10'

$IconOpen = New-Object Windows.Controls.Image
$IconOpen.Source = Get-SystemIcon -index 4  # Ícono de carpeta
$IconOpen.Width = 20
$IconOpen.Height = 20

$StackPanelOpen = New-Object Windows.Controls.StackPanel
$StackPanelOpen.Orientation = 'Horizontal'
$StackPanelOpen.HorizontalAlignment = 'Center'
$StackPanelOpen.Children.Add($IconOpen)
$StackPanelOpen.Children.Add($ButtonOpenFile)

$Grid.Children.Add($StackPanelOpen)
[Windows.Controls.Grid]::SetRow($StackPanelOpen, 0)

### BOTÓN "EJECUTAR"
$ButtonRun = New-Object Windows.Controls.Button
$ButtonRun.Content = "Ejecutar"
$ButtonRun.Width = 150
$ButtonRun.Height = 40
$ButtonRun.Margin = '10'

$IconRun = New-Object Windows.Controls.Image
$IconRun.Source = [System.Windows.Media.Imaging.BitmapImage]::new([uri]"https://cdn-icons-png.flaticon.com/512/109/109617.png")
$IconRun.Width = 20
$IconRun.Height = 20

$StackPanelRun = New-Object Windows.Controls.StackPanel
$StackPanelRun.Orientation = 'Horizontal'
$StackPanelRun.HorizontalAlignment = 'Center'
$StackPanelRun.Children.Add($IconRun)
$StackPanelRun.Children.Add($ButtonRun)

$Grid.Children.Add($StackPanelRun)
[Windows.Controls.Grid]::SetRow($StackPanelRun, 1)

### BOTÓN "INSTALAR"
$ButtonInstall = New-Object Windows.Controls.Button
$ButtonInstall.Content = "Instalar"
$ButtonInstall.Width = 150
$ButtonInstall.Height = 40
$ButtonInstall.Margin = '10'

$IconInstall = New-Object Windows.Controls.Image
$IconInstall.Source = [System.Windows.Media.Imaging.BitmapImage]::new([uri]"https://cdn-icons-png.flaticon.com/512/1828/1828817.png")
$IconInstall.Width = 20
$IconInstall.Height = 20

$StackPanelInstall = New-Object Windows.Controls.StackPanel
$StackPanelInstall.Orientation = 'Horizontal'
$StackPanelInstall.HorizontalAlignment = 'Center'
$StackPanelInstall.Children.Add($IconInstall)
$StackPanelInstall.Children.Add($ButtonInstall)

$Grid.Children.Add($StackPanelInstall)
[Windows.Controls.Grid]::SetRow($StackPanelInstall, 2)

# Acción para abrir fichero
$ButtonOpenFile.Add_Click({
    $OpenFileDialog = New-Object Microsoft.Win32.OpenFileDialog
    $OpenFileDialog.Filter = "Todos los archivos|*.*"
    if ($OpenFileDialog.ShowDialog()) {
        [System.Windows.MessageBox]::Show("Archivo seleccionado: " + $OpenFileDialog.FileName, "Archivo Seleccionado")
    }
})

# Acción para ejecutar (solo mensaje)
$ButtonRun.Add_Click({
    Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c exec.bat"
    [System.Windows.MessageBox]::Show("Ejecutando...", "Ejecutar")
})

# Acción para instalar (ejecutar setup.bat y exec.bat)
$ButtonInstall.Add_Click({
    Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c setup.bat"
    [System.Windows.MessageBox]::Show("Instalado.", "Instalar")
})

# Mostrar la ventana
$Window.ShowDialog()
