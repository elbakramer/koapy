Function New-TemporaryDirectory {
    $Parent = [System.IO.Path]::GetTempPath()
    [string] $Name = [System.Guid]::NewGuid()
    New-Item -ItemType Directory -Path (Join-Path "$Parent" "$Name")
}

Function Invoke-DownloadFile {
    Param (
        $Address,
        $FilePath
    )
    (New-Object System.Net.WebClient).DownloadFile("$Address", "$FilePath")
}

Function Get-OpenAPISetupFile {
    Param (
        $FilePath
    )
    $SetupFile = "OpenAPISetup.exe"
    $SetupFileURL = "https://download.kiwoom.com/web/openapi/$SetupFile"
    Invoke-DownloadFile -Address "$SetupFileURL" -FilePath "$FilePath"
}

Function Start-OpenAPISetupProcess {
    Param (
        $ISSFilePath
    )
    Write-Output "Creating Temporary Directory"
    $TempDir = New-TemporaryDirectory
    Write-Output "Created Temporary Directory: $TempDir"
    Try {
        $SetupFile = "OpenAPISetup.exe"
        $SetupFilePath = "$TempDir\$SetupFile"
        Write-Output "Downloading Installer"
        Get-OpenAPISetupFile -FilePath "$SetupFilePath"
        Write-Output "Downloaded Installer Location: $SetupFilePath"
        If ($ISSFilePath.EndsWith("\install.iss")) {
            Write-Output "Installing OpenAPI"
        }
        ElseIf ($ISSFilePath.EndsWith("\uninstall.iss")) {
            Write-Output "Uninstalling OpenAPI"
        }
        Write-Output "Starting Installer Process with ISSFile: $ISSFilePath"
        Start-Process -WorkingDirectory "$TempDir" -FilePath "$SetupFilePath" -ArgumentList "/s /f1`"$ISSFilePath`"" -Wait
        Write-Output "Installer Process Finished"
        If ($ISSFilePath.EndsWith("\install.iss")) {
            Write-Output "Installed OpenAPI"
        }
        ElseIf ($ISSFilePath.EndsWith("\uninstall.iss")) {
            Write-Output "Uninstalled OpenAPI"
        }
    }
    Finally {
        Remove-Item "$TempDir" -Recurse -ErrorAction Ignore
    }
}

Function Install-OpenAPI {
    Start-OpenAPISetupProcess -ISSFilePath "$PSScriptRoot\install.iss"
}

Function Uninstall-OpenAPI {
    Start-OpenAPISetupProcess -ISSFilePath "$PSScriptRoot\uninstall.iss"
}

Install-OpenAPI
