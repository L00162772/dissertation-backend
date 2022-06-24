# dissertation-backend
Backend Repository for the Dissertation practical element
 
## Folder Structure
terraform: Infrastructure as Code (IaC)

backend: backend code
 
## Terraform Instructions
### Prequisite Software:
Terraform: https://www.terraform.io/

### Run terraform code
For best results - it is recommended to follow the deployment process outlined in the Wiki https://github.com/L00162772/dissertation-backend/wiki/Deployment-Process for testing the code. Running terraform locally will required that some variables and attributes are tweaked. The code that is checked in has been tested using the deployment process and terraform cloud.

#### Execute plan
```
cd terraform
terraform init
terraform plan
```

#### Create Infrastructure
```
cd terraform
terraform apply --auto-approve
```

#### Destroy Infrastructure
```
cd terraform
terraform destroy --auto-approve
```


## Backend Instructions
### Prequisite Software:
NodeJs: https://nodejs.org/en/

### Run backend project
```
cd backend
npm install
npm start
```
