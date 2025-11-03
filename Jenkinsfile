pipeline {
  agent { label 'worker' }  // label of your agent node
  environment {
    AWS_DEFAULT_REGION = "us-east-1"
    ECR_REGISTRY = "030172394996.dkr.ecr.us-east-1.amazonaws.com"
    ECR_REPOSITORY = "my-app"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', credentialsId: 'github-creds-id', url: 'https://github.com/naveenseema/git-lab.git'
      }
    }

  stage('Login to ECR') {
      steps {
        withAWS(credentials: 'aws-creds', region: "${AWS_DEFAULT_REGION}") {
          sh '''
            aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
            docker login --username AWS --password-stdin ${ECR_REGISTRY}
          '''
        }
      }
    }

    stage('Build & Push Image') {
      steps {
        sh """
          docker build -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
          docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
          docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
        """
      }
    }

    stage('Deploy to EKS') {
      steps {
        // assume agent has awscli, kubectl, and proper kubeconfig (or create kubeconfig now)
        sh """
          aws eks update-kubeconfig --name demo-eks-lab --region ${AWS_DEFAULT_REGION}
          kubectl set image deployment/my-app my-app=${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} --record
         else
          echo "Deployment not found — applying manifests..."
          kubectl apply -f deployment.yaml
          kubectl apply -f service.yaml
        fi
        """
      }
    }
  }

  post {
    success {
      echo "Pipeline completed successfully."
    }
    failure {
      echo "Pipeline failed."
    }
  }
}
