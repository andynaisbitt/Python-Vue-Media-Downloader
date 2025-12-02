# Create Tutorial Structure for IT Apprentice Beta
$basePath = "C:\Gitlab Projects\ITAppBeta\src\components\Tutorials"

$tutorialStructure = @{
    "FirstDayIT" = @{
        "ActiveDirectoryBasics" = @{
            Sections = @(
                "IntroToAD",
                "UserManagement",
                "GroupBasics",
                "PasswordResets"
            )
        }
        "WindowsTroubleshooting" = @{
            Sections = @(
                "EventViewer",
                "TaskManager",
                "CommonIssues",
                "QuickFixes"
            )
        }
    }
    "CommandLine" = @{
        "BasicCommands" = @{
            Sections = @(
                "GettingStarted",
                "FileOperations",
                "NetworkCommands",
                "SystemInfo"
            )
        }
        "ScriptingBasics" = @{
            Sections = @(
                "IntroToScripting",
                "BatchFiles",
                "PowerShellBasics",
                "AutomationExamples"
            )
        }
    }
    "IdiotsWelcome" = @{
        "PrinterFixes" = @{
            Sections = @(
                "CommonPrinterIssues",
                "NetworkPrinters",
                "DriverManagement",
                "Troubleshooting"
            )
        }
        "WiFiBasics" = @{
            Sections = @(
                "ConnectionBasics",
                "CommonProblems",
                "RouterSetup",
                "TroubleshootingSteps"
            )
        }
    }
    "HardwareBasics" = @{
        "PCUpgrades" = @{
            Sections = @(
                "ComponentBasics",
                "RAMUpgrades",
                "StorageUpgrades",
                "SafetyGuidelines"
            )
        }
        "NetworkingGear" = @{
            Sections = @(
                "NetworkHardware",
                "CablingBasics",
                "RouterSetup",
                "TroubleshootingGuide"
            )
        }
    }
    "EthicalHacking" = @{
        "WiFiSecurity" = @{
            Sections = @(
                "SecurityBasics",
                "CommonVulnerabilities",
                "SecurityTools",
                "PreventionGuide"
            )
        }
        "PasswordHacking" = @{
            Sections = @(
                "PasswordSecurity",
                "CommonAttacks",
                "DefensiveMeasures",
                "BestPractices"
            )
        }
    }
    "SoftwareDevelopment" = @{
        "PythonBasics" = @{
            Sections = @(
                "FileAutomation",
                "APIsWithPython",
                "DataProcessing",
                "AutomationScripts"
            )
        }
        "CSharpBasics" = @{
            Sections = @(
                "ConsoleApps",
                "LINQExamples",
                "FileHandling",
                "BasicWinForms"
            )
        }
        "AutomationBasics" = @{
            Sections = @(
                "BatchScripts",
                "PowerShellScripts",
                "TaskScheduling",
                "ErrorHandling"
            )
        }
    }
    "WebDevelopment" = @{
        "HTMLBasics" = @{
            Sections = @(
                "BuildingPage",
                "DeployingPage",
                "BasicStyling",
                "ResponsiveDesign"
            )
        }
        "JavaScriptBasics" = @{
            Sections = @(
                "SimpleScripts",
                "FetchAPI",
                "DOMManipulation",
                "EventHandling"
            )
        }
        "Frameworks" = @{
            Sections = @(
                "ReactBasics",
                "VueBasics",
                "ComponentDesign",
                "StateManagement"
            )
        }
    }
    "Productivity" = @{
        "OfficeShortcuts" = @{
            Sections = @(
                "ExcelShortcuts",
                "WordShortcuts",
                "OutlookTips",
                "PowerPointHacks"
            )
        }
        "TimeManagement" = @{
            Sections = @(
                "ToolsOverview",
                "TimeBlocking",
                "TaskPrioritization",
                "ProductivityApps"
            )
        }
    }
}

# Create directory structure function
function Create-TutorialStructure {
    param (
        [string]$basePath,
        [hashtable]$structure
    )

    foreach ($category in $structure.Keys) {
        $categoryPath = Join-Path $basePath $category
        
        if (!(Test-Path $categoryPath)) {
            New-Item -Path $categoryPath -ItemType Directory -Force
            Write-Host "Created category directory: $category" -ForegroundColor Green
        }

        foreach ($tutorial in $structure[$category].Keys) {
            $tutorialPath = Join-Path $categoryPath $tutorial
            
            # Create tutorial folders
            @(
                "$tutorialPath",
                "$tutorialPath\sections",
                "$tutorialPath\config"
            ) | ForEach-Object {
                if (!(Test-Path $_)) {
                    New-Item -Path $_ -ItemType Directory -Force
                    Write-Host "Created directory: $_" -ForegroundColor Green
                }
            }

            # Create base files
            @(
                "$tutorialPath\TutorialOverview.tsx",
                "$tutorialPath\config\tutorialData.ts"
            ) | ForEach-Object {
                if (!(Test-Path $_)) {
                    New-Item -Path $_ -ItemType File -Force
                    Write-Host "Created file: $_" -ForegroundColor Green
                }
            }

            # Create section files
            foreach ($section in $structure[$category][$tutorial].Sections) {
                $sectionPath = "$tutorialPath\sections\$section.tsx"
                if (!(Test-Path $sectionPath)) {
                    New-Item -Path $sectionPath -ItemType File -Force
                    Write-Host "Created section file: $section.tsx" -ForegroundColor Green
                }
            }
        }
    }
}

# Execute structure creation
try {
    Create-TutorialStructure -basePath $basePath -structure $tutorialStructure
    Write-Host "Tutorial structure created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error creating tutorial structure: $_" -ForegroundColor Red
}