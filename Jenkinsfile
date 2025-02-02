#!/usr/bin/env groovy

def defineBranchName() {
    def branchName = "${env.BRANCH_NAME}"
    branchName = branchName.replace ('/', '-')
    branchName = branchName.replace ('_', '-')
    branchName = branchName.replace ('.', '')
    return branchName
}

def defineImageName() {
    def branchName = defineBranchName()
    return "${branchName}-b${BUILD_NUMBER}"
}

def commitMessage() {
    def message = sh(returnStdout: true, script: "git log --format='medium' -1 ${GIT_COMMIT}").trim()
    return "${message}"
}

def defineDockerTag() {
    def branchName = "${env.BRANCH_NAME}"
    branchName = branchName.replace ('/', '')
    branchName = branchName.replace ('_', '')
    branchName = branchName.replace ('.', '')
    return "${branchName}b${BUILD_NUMBER}"
}

def projectName() {
  def jobNameParts = env.JOB_NAME.tokenize('/') as String[]
  return jobNameParts.length < 2 ? env.JOB_NAME : jobNameParts[jobNameParts.length - 2]
}

pipeline{
	agent any
	
	environment {
		BRANCH = "${BRANCH_NAME}"
		registry="registry.digitalocean.com/spacelaunchnow-registry/sln-server"
		registryURL = "https://registry.digitalocean.com/spacelaunchnow-registry/sln-server"
		registryCredential = 'digitalocean_registry'
		dockerTag = defineDockerTag()
        imageName = defineImageName()
		branchName = defineBranchName()
		dockerImage = ''
        DISCORD_URL = credentials('DiscordURL')
        COMMIT_MESSAGE = commitMessage()
        PROJECT_NAME = projectName()
	}
	
	stages{
		stage('Build Docker Image'){
			steps{
				script{
                    if (env.BRANCH_NAME == 'master') {
                        withCredentials([file(credentialsId: 'SLNProductionConfig', variable: 'configFile')]) {
                            sh 'cp $configFile src/spacelaunchnow/config.py'
                        }
                    } else {
                        withCredentials([file(credentialsId: 'SLNConfig', variable: 'configFile')]) {
                            sh 'cp $configFile src/spacelaunchnow/config.py'
                        }
                    }
					if(!fileExists("Dockerfile")){
						echo "No Dockerfile";
					} else {
					    withCredentials([string(credentialsId: 'EXTRA_INDEX_URL', variable: 'INDEX_URL')]) {
                            def buildArg = '--build-arg EXTRA_INDEX_URL="$INDEX_URL" .'
                            def dockerReg = registry + ":" + imageName
                            dockerImage = docker.build(dockerReg, buildArg)
                        }
					}
				}
			}
		}
        stage('Run Tests') {
            steps {
              sh "docker run --rm ${registry}:${imageName} coverage run /code/manage.py test --settings=spacelaunchnow.settings.test"
            }
        }
		stage('Deploy Docker Image'){
			steps{
				script{
					docker.withRegistry(registryURL, registryCredential){
						dockerImage.push()
						if (env.BRANCH_NAME == 'master') {
						    dockerImage.push("${dockerTag}")
						    dockerImage.push("production")
						} else {
                            dockerImage.push("${dockerTag}")
						}
					}
				}
			}
		}
		stage('Deploy Helm Release'){
            when {
                branch 'master'
            }
		    steps {
		        script {
                    sh '''
                        kubectl config use-context do-nyc1-k8s-spacelaunchnow-dev
                        export STAGING_NAMESPACE=sln-prod
                        export RELEASE_NAME=sln-prod-app
                        export DEPLOYS=$(helm ls --all-namespaces | grep $RELEASE_NAME | wc -l)
                        if [ $DEPLOYS  -eq 0 ];
                        then
                            helm install $RELEASE_NAME k8s/helm/ --namespace=$STAGING_NAMESPACE --values k8s/helm/values.yaml;
                        else
                            helm upgrade $RELEASE_NAME k8s/helm/ --namespace=$STAGING_NAMESPACE --values k8s/helm/values.yaml --recreate-pods;
                        fi
                    '''
		        }
		    }
		}
    }
    post {
        always {

            discordSend description: "**Status:** ${currentBuild.currentResult}\n**Branch: **${env.BRANCH_NAME}\n**Build: **${env.BUILD_NUMBER}\n\n${COMMIT_MESSAGE}\n\nLink: https://" + imageName + "-staging.calebjones.dev",
                footer: "",
                link: env.BUILD_URL,
                result: currentBuild.currentResult,
                title: PROJECT_NAME,
                webhookURL: DISCORD_URL,
                thumbnail: "https://i.imgur.com/FASV6fJ.png",
                notes: "Hey <@&641718676046872588>, new build completed for ${PROJECT_NAME}!"
            // This needs to be removed in favor of removing credential files instead.
            sh '''
               rm src/spacelaunchnow/config.py
               '''
            always {
                archiveArtifacts artifacts: 'build/xmlrunner/*.xml', fingerprint: true
                junit 'build/xmlrunner/*.xml'
            }
        }
    }
}