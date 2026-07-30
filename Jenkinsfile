#!groovy
// @Library(['abi@3.7.0rc3', 'idf-enabling@validate_precheck_waiver']) _

// import owm.common.BuildInfo
// Map buildinfo = BuildInfo.instance.data

def TimerEvent = false
def UserEvent = false
def PushEvent = false

def agentLabel = "win"
def agentVMWorkspace = "C:/jenkins/workspace/SampleWS"
def agentWorkspace = "C:/home/jenkins/agent/workspace/SampleWS"
def defaultMainBranch = "OWR-69837_precheck_report_waiver"

def podCloud = "winidoc"
def ContainerName = "build-environment"
def ContainerType = "windows"

def IntelSign = false
def MSFTPreProdSign = false
def OneBkcBuildInfo = false
def EnablePrecheckWaiverReport = false

pipeline {

    // agent {
    //     kubernetes {
    //         cloud podCloud
    //         defaultContainer ContainerName
    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
    //         customWorkspace agentWorkspace
    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
    //     }
    // }

    agent none

    // Parameters for the Jenkins GUI.  It is recommended to not change them in the Jenkinsfile unless you are trying to change the Jenkins GUI.
    // Parameters take +1 cycle to adopt the change.  Ie If you change a defaultValue below and push, the first run the defaultValue will be the old value.
    // All subsequent runs will have the new default value.
    parameters {
        booleanParam(name: 'ReleaseBuild', defaultValue: false, description: 'Enable for Release Build trigger')
        string(name: 'BranchName', defaultValue: defaultMainBranch, description: 'Input BranchName for the Repository when executed as Single Branch Pipeline')
        string(name: 'VersionNumber', defaultValue: '', description: 'Use this version number for build (if empty the number will be derived from the Build Version Prefix in the Jenkinsfile)')
        string(name: 'EWDK', defaultValue: '22000.Co.1052', description: 'Version of the EWDK to use (default: uses value in Manifest.xml)')
        booleanParam(name: 'BullseyeCoverage', defaultValue: false, description: 'Enable to run Bullseye Coverage')
        booleanParam(name: 'SecureCoverityScan', defaultValue: false, description: 'Enable to run Secure Coverity Scan')
        booleanParam(name: 'SecureCoverityScanFS', defaultValue: false, description:'Enable to run SecureCoverityScanFS')
        booleanParam(name: 'StaticCodeScan', defaultValue: false, description: 'Enable to run Static Code Scan')
        booleanParam(name: 'BanditScan', defaultValue: false, description: 'Enable to run Bandit Scan')
        booleanParam(name: 'VulnerabilityScan', defaultValue: false, description: 'Enable to run Vulnerability Scan')
        booleanParam(name: 'IpScan', defaultValue: false, description: 'Enable to run IP Scan')        
        booleanParam(name: 'BinaryScan', defaultValue: false, description: 'Enable to run BDBA and SSCB Scans')        
        booleanParam(name: 'PreProdSign', defaultValue: false, description: 'Enable MTCD PreProdSign')
        booleanParam(name: 'ProdAttest', defaultValue: false, description: 'Enable MTCD ProdAttest')
        booleanParam(name: 'IntelSign', defaultValue: false, description: 'Enable to Sign Binaries with Intel Signing')
        booleanParam(name: 'ArtifactsDeploy', defaultValue: false, description: 'Enable to Deploy to Artifactory')
        booleanParam(name: 'PreChecks', defaultValue: false, description: 'Enable to run PreChecks')
        booleanParam(name: 'PreChecksWaiverReport', defaultValue: false, description: 'Enable to run Waiver Report for PreChecks')
        booleanParam(name: 'SdleAutomation', defaultValue: false, description: 'Enable SDLe Automation')
        booleanParam(name: 'SdleAutomationDryRun', defaultValue: false, description: 'Enable SDLe Automation in DryRun Mode')
        string(name: 'SdleUrl', defaultValue: 'https://sdl-e.app.intel.com/project?id=a9033ecb-bd47-4102-ad97-0b7878dd95bd', description: 'Enter SDLe Submission URL e.g. https://sdl-e.app.intel.com/project?id=3e0f5f68-76b9-4129-823d-b68492c70f78')
        string(name: 'SdleId', defaultValue: '15309', description: 'Enter SDLe Project ID e.g. 8976')
        booleanParam(name: 'SBOMGenSign', defaultValue: false, description: 'Enable SBOM Generation and Signing')
        string(name: 'IPXOwnerEmailId', defaultValue: 'vasanth.shivakumar@intel.com', description: 'Enter the Ingredient IPX Owner EmailID  e.g. vasanth.shivakumar@intel.com')
        string(name: 'ContainerImage', defaultValue: 'amr-registry.caas.intel.com/owr/abi_windows_1809-3406:3.6.0', description: 'Enter Container Image to execute the Pipeline')
        booleanParam(name: 'GetUpStreamVersionEvents', defaultValue: false, description: 'Get Event Details from UpStream Job')
        booleanParam(name: 'TimerEvent', defaultValue: false, description: 'Timer Event From UpStream Job')
        booleanParam(name: 'UserEvent', defaultValue: false, description: 'User Event From UpStream Job')
        booleanParam(name: 'PushEvent', defaultValue: false, description: 'Push Event From UpStream Job')
    }

    environment {
        BuildVersionPrefix = '1.0.00'
        HTTP_PROXY = "http://proxy-dmz.intel.com:912"
        HTTPS_PROXY = "http://proxy-dmz.intel.com:912"
        NO_PROXY = "intel.com,.intel.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8,134.134.0.0/16"
        TicGenProjectName = "samplewin-ticgen"
        IngredientName = "SampleWin"
        IngredientPath = "SampleWin/windows"
        CheckoutPath = "SampleWin"
        BuildConfig = "IDF/BuildConfig.json"
        Manifest = "IDF/Manifest.xml"
        Platform = "x64"
        Config = "Release"
        EWDK = "22000.Co.1052"
        CoverityStream = "CCG-ADO-BA-SAMPLE-WINDOWS-C-DEVELOP"
        CoverityCSharpStream = "CCG-ADO-BA-SAMPLE-WINDOWS-CSHARP-DEVELOP"
        CoverityStreamFS = "CCG-ADO-BA-SAMPLE-WINDOWS-FS"
        // App Src Paths
        ScriptAppPath = "PythonApp/todoapp/todoapp.py"
        PythonAppPath = "PythonApp/todoapp/todoapp.py"
        ManifestFile = "PythonApp/todoapp/requirements.txt"
        // Test Coverage Paths 
        PythonAppTestCoveragePath = "Documents/PyCoverage"
        // Bin Paths
        IntelSignDriverInf = "Drivers/Release/*.inf"
        DriverBinPath = "Drivers/Release"
        AppBinPath = "Apps/Service/Release"
        CSharpAppBinPath = "Apps/CSharpApp/Release"
        CMakeAppBinPath = "Apps/CMakeApp/Release"
        PythonAppBinPath = "Apps/PythonApp/Release"
        PythonExe = "C:/Python312/python"
        // OneBOM/SBOM Env Variables
        IngredientOneBOMPath = "IDF/OneBomPrechecks"
        IngredientOneBOMWorkSheetName = "Bill of Materials"
        OneBOMProjectName = "SampleWin"
        IgnoreOneBOMComponent = "sample_windows"
        ExcludeBuildBinFolders = "Drivers-MsftSign,Drivers-MsftProdAttest,Apps,Documents"
        // ABI_CONTAINER = "TRUE"
        ContainerNode = true
        SkipGitReference = true
        sfsdk_is_dev = true
        ContainerType = "windows"
        // Precheck Env Variables
        PrecheckIngredientPath = "IDF/OneBomPrechecks"
        PrecheckIngredientType = "driver"
        PrecheckWaiverReportPlatformConfig = "NVL-HX-CORP"
        // Vulnerability Env Variables
        VulnerabilityScanDockerFile = "PythonApp/todoapp/Dockerfile"
        VulnerabilityScanDockerImage = "\"amr-registry.caas.intel.com/owr/idf2/pythonapp/win:1.0\""
        BRANCH_NAME = "${params.BranchName}"
    }

    options {
        timeout(time: 300, unit: 'MINUTES')
        timestamps()
        // skipDefaultCheckout true  // Disabled: Initialize() which handled custom checkout is commented out
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
    }

    stages {
        // stage("GetBuildVersion") {
        //     steps {
        //         script {
        //             if (params.GetUpStreamVersionEvents) {
        //                 (TimerEvent, UserEvent, PushEvent) = GetUpStreamVersionEvents()
        //             } else {
        //                 (TimerEvent, UserEvent, PushEvent) = GenerateBuildVersion()
        //             }   
        //             BuildInfo.instance.data["Version"] = env.BuildVersion
        //         }
        //     }
        // } // end GetBuildVersion stage
        stage("Init") {
            // agent {
            //     kubernetes {
            //         cloud podCloud
            //         defaultContainer ContainerName
            //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
            //         customWorkspace agentWorkspace
            //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
            //     }
            // }
            steps {
                script {
                    
                    TimerEvent = params.TimerEvent
                    UserEvent = params.UserEvent
                    PushEvent = params.PushEvent

                    echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                    // Initialize()
                    
                    IntelSign = params.IntelSign
                    MSFTPreProdSign = params.PreProdSign
                    EnablePrecheckWaiverReport = params.PreChecksWaiverReport
                    
                    if (env.BRANCH_NAME == "${defaultMainBranch}" && (params.ReleaseBuild || TimerEvent)) {
                        IntelSign = true
                        if (params.ReleaseBuild) {
                            env.MsftPreProdSignDriverInf = "Drivers-MsftSign/Release/*.inf"
                            MSFTPreProdSign = true
                            EnablePrecheckWaiverReport = true
                            echo "Release Build Triggered. IntelSign, MSFTPreProdSign and EnablePrecheckWaiverReport are set to true."
                        }
                    } else {
                        echo "IntelSign, MSFTPreProdSign and EnablePrecheckWaiverReport are set to false."
                    }
                }
            }
        } // end Init stage
        stage("BuildAndScan") {
            parallel {
                stage("SampleWinDriver") {
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // BuildIngredient(SubComponents: "SampleWinDriver", IntelSign: IntelSign, IntelProdSignDrivers: true, MtcdPreProdSignDrivers: MSFTPreProdSign, MtcdProdAttestDrivers: params.ProdAttest)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "BuildIngredient() is called here."
                        }
                    }
                } // end SampleWinDriver stage
                stage("CSharpApp") {
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    environment {
                        Platform = "AnyCPU"
                        Config = "Release"
                    }
                    steps {
                        script {
                            // BuildIngredient(SubComponents: "CSharpApp", IntelSign: IntelSign, IntelProdSignDrivers: true)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "CSharpApp BuildIngredient() is called here."
                        }
                    }
                } // end CSharpApp stage
                stage("CMakeApp") {
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // BuildIngredient(SubComponents: "CMakeApp,CMakeAppExe,CMakeAppTests", IntelSign: IntelSign)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "CMakeApp BuildIngredient() is called here."
                        }
                    }
                } // end CMakeApp stage
                stage("PythonApp") {
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // BuildIngredient(SubComponents: "PythonApp,PythonAppExe,PythonAppTests", IntelSign: IntelSign)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "PythonApp BuildIngredient() is called here."
                        }
                    }
                } // end PythonApp stage
                stage("BullseyeCoverage") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.BullseyeCoverage == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            env.bullseyeCoverageReport = "Documents/Bullseye/Bullseye_Report*html.zip"
                            // BullseyeCoverage(SubComponents: "CMakeApp,CMakeAppExe,CMakeAppTests")
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "BullseyeCoverage() is called here."
                        }
                    }
                } //end BullseyeCoverage Stage                 
                stage("BanditScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.BanditScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // BanditScan()
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "BanditScan() is called here."
                        }
                    }
                } //end BanditScan Stage
                stage("VulnerabilityScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.VulnerabilityScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // TrivyScan(PythonApp: true, PythonExe: PythonExe)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "TrivyScan() is called here."
                        }
                    }
                } //end VulnerabilityScan Stage
                stage("VulnerabilityDockerImageScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.VulnerabilityScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // TrivyScan(ScanType: "image",
                            //     IngredientName: "container_report_${IngredientName}",
                            //     DockerImage: "${VulnerabilityScanDockerImage}"
                            // )
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "TrivyScan() is called here."
                        }
                    }
                } //end VulnerabilityDockerImageScan Stage
                stage("VulnerabilityDockerFileScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.VulnerabilityScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // TrivyScan(ScanType: "config",
                            //     IngredientName: "dockerfile_report_${IngredientName}",
                            //     ManifestFile: "${VulnerabilityScanDockerFile}"
                            // )
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "TrivyScan() is called here."
                        }
                    }
                } //end VulnerabilityDockerfileScan Stage
                stage("ProtexScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.IpScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // ProtexScan()
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "ProtexScan() is called here."
                        }
                    }
                } //end ProtexScan Stage
                stage("SecureCoverityScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.SecureCoverityScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // CoverityScan()
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "CoverityScan() is called here."
                        }
                    }
                } //end SecureCoverityScan Stage
                stage("SecureCoverityScanCSharp") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.SecureCoverityScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // CoverityScan(CoverityStreamToScan: env.CoverityCSharpStream.toString(), Platform: "AnyCPU", Config: "Release", CSharpCheckers: true)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "CoverityScan() is called here."
                        }
                    }
                } //end SecureCoverityScanCSharp Stage
                stage("SecureCoverityScanFS") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.SecureCoverityScanFS == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // CoverityScan(CoverityStreamToScan: env.CoverityStreamFS, Ignore: '".*IDF.*",".*Documents.*"', FsCapture: true)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "CoverityScan() is called here."
                        }
                    }
                } //end SecureCoverityScanFS Stage
                stage("StaticCodeScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.StaticCodeScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // SemmleScan(SubComponents: "SampleWinDriver")
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "SemmleScan() is called here."
                        }
                    }
                } //end StaticCodeScan Stage
            } // end parallel
        } // end of BuildAndScan stage
        stage("BinaryScans") {
            parallel {
                stage("SBOM") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.SBOMGenSign == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            // Generate SBOM SPDX Artifact
                            // SBOMGen(ArtifactPackageName: ["BuildBin-SampleWinDriver*"], ExcludeBuildBinFolders: env.ExcludeBuildBinFolders, PostBuildWorkspaceCleanup: false)
                            echo "SBOMGen() is called here."

                            // Check SBOM SPDX Signing Flow (DryRun/Production)
                            def IsProd = false
                            if (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) {
                                IsProd = true
                                echo "SBOM Signing Flow is set to Production."
                            }

                            // Sign SBOM SPDX Artifact
                            // SBOMSign(IsProd: IsProd)
                            echo "SBOMSign() is called here."
                        }
                    }
                } // end SBOM
                stage("BDBAScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.BinaryScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // BdbaBinaryScan()
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "BdbaBinaryScan() is called here."
                        }
                    }
                } // end BDBAScan
                stage("SSCBScan") {
                    when {
                        expression {
                            (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                            params.BinaryScan == true ||
                            (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)
                        }
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // SscbBinaryScan()
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "SscbBinaryScan() is called here."
                        }
                    }
                } // end SSCBScan
            } // parallel
        } // end BinaryScans
        stage("ArtifactGenDeploy") {
            parallel {
                stage("ArtifactGen") {
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            if ((env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) || (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true)) {
                                // ArtifactGenDeploy(BullseyeCoverage: true, SecureCoverityScanFS: true, SecureCoverityScan: true, StaticCodeScan: true, BanditScan: true,  VulnerabilityScan: true, IpScan: true, BinaryScan: true, IntelSign: IntelSign, ArtifactsDeploy: true, PreProdSign: MSFTPreProdSign, ProdAttest: params.ProdAttest, OneBkcBuildInfo: OneBkcBuildInfo, Sdle: true, SBOM: true, SkipBinaryScans: true)
                                echo "ArtifactGenDeploy() is called here."
                            } else {
                                // ArtifactGenDeploy(BullseyeCoverage: params.BullseyeCoverage, SecureCoverityScanFS: params.SecureCoverityScanFS, SecureCoverityScan: params.SecureCoverityScan, StaticCodeScan: params.StaticCodeScan, BanditScan: params.BanditScan, VulnerabilityScan: params.VulnerabilityScan, IpScan: params.IpScan, BinaryScan: params.BinaryScan, IntelSign: IntelSign, ArtifactsDeploy: params.ArtifactsDeploy, PreProdSign: params.PreProdSign, ProdAttest: params.ProdAttest, SBOM: params.SBOMGenSign, SkipBinaryScans: true)
                                echo "ArtifactGenDeploy() is called here."
                            }
                        }
                    }
                } //end ArtifactGen Stage
            } // end parallel
        } // end of ArtifactGenAndDeploy stage
        stage("PreChecks") {
            when{
                expression {
                    (env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true) ||
                    (env.BRANCH_NAME == "${defaultMainBranch}" && TimerEvent == true) ||
                    params.PreChecks == true
                }
            }
            // agent {
            //     kubernetes {
            //         cloud podCloud
            //         defaultContainer ContainerName
            //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
            //         customWorkspace agentWorkspace
            //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
            //     }
            // }
            steps {
                script {
                    // PreChecks(IngredientPrecheckPath: env.PrecheckIngredientPath,
                    //           IngredientVersion: env.BuildVersion,
                    //           IngredientName: env.IngredientName,
                    //           IngredientType: env.PrecheckIngredientType,
                    //           IngredientPackageName: "${env.IngredientName}_${env.BuildVersion}",
                    //           EnableWaiverReport: EnablePrecheckWaiverReport,
                    //           PlatformConfig: env.PrecheckWaiverReportPlatformConfig)
                    echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent} and EnablePrecheckWaiverReport: ${EnablePrecheckWaiverReport}"
                    echo "PreChecks() is called here."
                }
            }
        } // end of Precheck
        stage("SDLeOneBOMAutomation") {
            parallel {
                stage("SDLe") {
                    when{
                        expression{(params.SdleAutomation == true || params.SdleAutomationDryRun == true) && env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true}
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            // SdleAutomation(nonMandatory: true)
                            echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                            echo "SdleAutomation() is called here."
                        }
                    }
                } // end SDLe
                stage("AutoBOM") {
                    when{
                        expression{env.BRANCH_NAME == "${defaultMainBranch}" && params.ReleaseBuild == true}
                    }
                    // agent {
                    //     kubernetes {
                    //         cloud podCloud
                    //         defaultContainer ContainerName
                    //         label "${env.STAGE_NAME}-${UUID.randomUUID().toString()}"
                    //         customWorkspace agentWorkspace
                    //         yaml GetSecurePodDefinitionYaml(ContainerType: ContainerType, ContainerImage: "", ContainerName: ContainerName)
                    //     }
                    // }
                    steps {
                        script {
                            if (env.IngredientOneBOMPath && env.IngredientOneBOMWorkSheetName && env.OneBOMProjectName) {
                                // AutoBOM()
                                echo "${env.BRANCH_NAME} branch and ReleaseBuild: ${params.ReleaseBuild} and TimerEvent: ${TimerEvent} and UserEvent: ${UserEvent} and PushEvent: ${PushEvent}"
                                echo "AutoBOM() is called here."
                            }
                        }
                    }
                } // end AutoBOM
            } // end parallel
        } // end of SDLeOneBOMAutomation
    } // end stages
    // post {
    //   always {
    //     script {
    //         PostActionParserNotifier(defaultMainBranch: defaultMainBranch, TimerEvent: TimerEvent)
    //     }
    //   }
    // }
} //end pipeline
