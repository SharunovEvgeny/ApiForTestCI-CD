# ICQApi
server for icq
Status of Last Deployment:<br>
<img src="https://github.com/SharunovEvgeny/ApiForTestCI-CD/workflows/TestCICD/badge.svg?branch=main"><br>




name: TestCICD
env:
  APPLICATIONS_NAME: "MyDjango"
  DEPLOY_PACKAGE_NAME: "dgango-deploy-ver-${{ github.sha }}"

# Run this workflow every time a new commit pushed to your repository
on:
  push:
    branches: 
      - main

jobs:
  my_test:
    name: HelloTest
    runs-on: ubuntu-latest
    steps:
      - name: Print Hello MessageTEst
        run : echo "Hello World from TEst"
        
      - name: Execure few commands
        run: |
          echo "Hello Message1"
          echo "Hellow Message2"
          echo "Applications name: ${{ env.APPLICATIONS_NAME }}"
          
      - name: Git clone my repo
        uses: actions/checkout@v1
        
      - name: Check folder
        run: ls -la
        
      - name: Check python
        run: python3 --version
        
      - name: Check docker
        run: |
          docker -v
          docker ps -a
  my_deploy:
    name: HelloDeploy
    runs-on: ubuntu-latest
    needs: [my_test]
    env:
      VAR1: "Var 1"
    steps:
      - name: Print Hello Message
        run : echo "Hello World from Deploy"
        
      - name: Execure few commands
        run: |
          echo "Hello Message1 ${{ env.VAR1 }}"
          echo "LOCAL VAR = $LOCAL_VAR"
          echo "Applications name: ${{ env.DEPLOY_PACKAGE_NAME }}"
        env:
          LOCAL_VAR: "SUper LOcal var"
    
