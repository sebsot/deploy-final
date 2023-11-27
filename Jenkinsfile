pipeline {
    
    agent any
    
    environment{
        NOMBRE_IMG = "py-flask-mysql"
    }
    
    stages {
        stage('Git Clone'){
            steps {
                git credentialsId: 'GITHUB_CREDENTIALS', url: 'https://github.com/sebsot/deploy-final'
            }
        }
    
        stage('test de la imagen') {
            steps {
                
                sh "docker-compose up -d --build"
                sleep(time:15, unit: "SECONDS")
            
                sh "docker exec flask-app-container python tests.py"

                sh "sudo rm -r data"
                
                sh "docker stop flask-app-container"
                sh "docker stop flask-app-db-container"
                
                sh "docker rm flask-app-container"
                sh "docker rm flask-app-db-container"

            }
        }
        
        stage('SonarQube Analysis') {
            steps{
                script{
                sh "docker start sonarqube"
                // sleep(time:60, unit: "SECONDS")
                withCredentials([string(credentialsId: 'USER_SONARQUBE', variable: 'USER_SONARQUBE'), string(credentialsId: 'PASS_SONARQUBE', variable: 'PASS_SONARQUBE')]){
                        def scannerHome = tool name: 'sonarscanner'
                        withSonarQubeEnv('SonarQube') {
                                sh "${scannerHome}/bin/sonar-scanner -Dsonar.login=${USER_SONARQUBE} -Dsonar.password=${PASS_SONARQUBE} -Dsonar.projectKey=jenkins-deploy -X"
                                        }
                                }
                        }
                }
        }
        stage('Build Docker Image'){
            steps {
                sh "docker-compose build"
            }
        }
    
    
    
       stage('Push Docker Image') {
           steps {
                withCredentials([string(credentialsId: 'USER_DOCKER', variable: 'USER_DOCKER'), string(credentialsId: 'PASS_DOCKER', variable: 'PASS_DOCKER')]) {
                    sh "docker login -u ${USER_DOCKER} -p ${PASS_DOCKER}"
                    sh "docker push ${USER_DOCKER}/flask-app"
                }
            }
       }

        
        stage('Deploy Kubernetes'){
            steps {
                script {
                    withCredentials([string(credentialsId: 'IP_PRODUCCION', variable: 'IP_PRODU'), string(credentialsId: 'USER_PRODUCCION', variable: 'USER_PRODU')]) 
                    {
            
                        def produccion = "${USER_PRODU}@${IP_PRODU}"
                        sh "mkdir -p /$HOME/deploy-final"
                        sh "scp -r Kubernetes ${produccion}:/$HOME/deploy-final"
                        // sh "ssh ${produccion} 'minikube start'"
                        sh "ssh ${produccion} 'kubectl apply -f \$(printf \"%s,\" $HOME/deploy-final/*.yaml | sed \"s/,\$//\")'"
                        sleep(time:4, unit: "SECONDS")
                        sh "ssh ${produccion} 'minikube service app --url'"
            
                        
                        def minikubeIp = sh(script:"ssh ${produccion} 'minikube ip'", returnStdout: true).trim()
                        def puerto = sh(script:"ssh ${produccion} 'kubectl get service app --output='jsonpath={.spec.ports[0].nodePort}' --namespace=default'", returnStdout: true).trim()
                        
                        sh(script: "echo ssh -L 192.168.229.134:${puerto}:${minikubeIp}:${puerto}")
                        
                        //sh "ssh ${produccion} 'kubectl delete deployments,services app db'" 
                        
                        sh "ssh ${produccion} 'rm /$HOME/deploy-final/*.yaml'"
                        sh "ssh ${produccion} 'rmdir /$HOME/deploy-final'"
                    }
                }
            }
        }
    }
}
