# путь к WinRAR 
$rar = 'C:\Program Files\WinRAR\Rar.exe' 
# куда архивируем личные папки 

$Logfile = 'E:\AWS\Logapp.log'
#Stage 1 backup C:
$Path = 'C:\BPMOnlineAppFiles\'
Remove-Item E:\AWS\CAPPS\*
ForEach ($n in  Get-ChildItem -Path  $Path -Force) {
$FilesArh = 'E:\AWS\CAPPS\' + $n + '.rar' 
$Dir = $Path  + $n
&$rar a "$FilesArh" $Dir  -r >> $LogFile 
echo $n + 'backuped'


}

#Stage 1 backup E:
$Path = 'E:\BPM\'
Remove-Item E:\AWS\EAPPS\*
ForEach ($n in  Get-ChildItem -Path  $Path -Force) {
$FilesArh = 'E:\AWS\EAPPS\' + $n + '.rar' 
$Dir = $Path  + $n
&$rar a "$FilesArh" $Dir  -r >> $LogFile 
echo $n + 'backuped'


}

#Stage 1 backup F:
$Path = 'F:\BPMAPPfiles\'
Remove-Item E:\AWS\FAPPS\*
ForEach ($n in  Get-ChildItem -Path  $Path -Force) {
$FilesArh = 'E:\AWS\FAPPS\' + $n + '.rar' 
$Dir = $Path  + $n
&$rar a "$FilesArh" $Dir  -r >> $LogFile 
echo $n + 'backuped'


}


echo  "success"
