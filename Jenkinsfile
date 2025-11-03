pipeline {
  agent { label 'worker' }

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
          sh """
            aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | \
            docker login --username AWS --password-stdin ${ECR_REGISTRY}
          """
        }
      }
    }

    stage('Build & Push Image') {
      steps {
        sh """
          echo "Building image tag: ${IMAGE_TAG}"
          docker build -t ${ECR_REPOSITORY}:${IMAGE_TAG} .
          docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
          docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
        """
      }
    }

    stage('Deploy to EKS') {
      steps {
        sh """
          echo "Deploying image tag: ${IMAGE_TAG} to EKS cluster..."
          aws eks update-kubeconfig --name demo-eks-lab --region ${AWS_DEFAULT_REGION}

          # Always update deployment to new image tag
          kubectl set image deployment/my-app my-app=${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} --record || true

          # Apply manifests if deployment doesn't exist
          if ! kubectl get deployment my-app >/dev/null 2>&1; then
            echo "Deployment not found — applying manifests..."
            kubectl apply -f deployment.yaml
            kubectl apply -f service.yaml
          fi

          kubectl rollout status deployment/my-app
          echo "Deployment updated to image tag ${IMAGE_TAG}"
        """
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline completed successfully for image tag ${IMAGE_TAG}"
    }
    failure {
      echo "❌ Pipeline failed."
    }
  }
}
