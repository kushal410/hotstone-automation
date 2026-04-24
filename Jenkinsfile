pipeline {
    agent any

    environment {
        LT_USERNAME = credentials('LT_USERNAME')
        LT_ACCESS_KEY = credentials('LT_ACCESS_KEY')
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_REPO/hotstone-automation.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m pip install --upgrade pip
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run LambdaTest Automation') {
            steps {
                sh '''
                python3 lamda.hot.py
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.png, **/*.xml', allowEmptyArchive: true
            junit '**/test-results.xml'
        }

        success {
            echo "✅ LambdaTest automation passed"
        }

        failure {
            echo "❌ LambdaTest automation failed"
        }
    }
}
