# Botón con ícono de carpeta para seleccionar archivo
$ButtonFile.Content = ""
$ButtonFile.ToolTip = "Seleccionar Archivo"

# Añadir icono al botón
$icono = New-Object System.Windows.Controls.Image
$icono.Source = [System.Windows.Media.Imaging.BitmapImage]::new((Resolve-Path ".\folder-icon.png").Path)
$icono.Width = 20
$icono.Height = 20
$ButtonFile.Content = $icono
