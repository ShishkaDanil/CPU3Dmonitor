[Setup]
AppName=CPU3Dmonitor
AppVersion=1.0
DefaultDirName={pf}\CPU3Dmonitor
DefaultGroupName=CPU3Dmonitor
OutputDir=.
OutputBaseFilename=setup

[Files]
Source: "dist\CPU3Dmonitor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\CPU3Dmonitor"; Filename: "{app}\CPU3Dmonitor.exe"
Name: "{startup}\CPU3Dmonitor"; Filename: "{app}\CPU3Dmonitor.exe"

[Run]
Filename: "{app}\CPU3Dmonitor.exe"; Description: "{cm:LaunchProgram,CPU3Dmonitor}"; Flags: nowait postinstall skipifsilent
