# dissertation-backend
Backend Repository for the Dissertation
See: https://andyjones.co/articles/react-aws-terraform-github-actions/
See: https://stackoverflow.com/questions/65242830/in-a-github-actions-workflow-is-there-a-way-to-have-multiple-jobs-reuse-the-sam
See: https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#about-matrix-strategies && https://github.community/t/can-i-share-strategy-matrices-between-multiple-jobs/195827/5 && https://docs.github.com/en/actions/using-workflows/reusing-workflows
See: https://stackoverflow.com/questions/67097661/how-to-pass-github-actions-user-input-into-a-python-script
See: https://github.com/actions/setup-python

## Folder Structure
terraform: Infrastructure as Code (IaC)
backend: backend code
 
## Terraform Instructions
### Prequisite Software:
Terraform: https://www.terraform.io/

### Run terraform code
#### Execute plan
cd terraform
terraform init
terraform plan

#### Create Infrastructure
cd terraform
terraform apply --auto-approve

#### Destroy Infrastructure
cd terraform
terraform destroy --auto-approve


## Backend Instructions
### Prequisite Software:
NodeJs: https://nodejs.org/en/

### Run backend project
cd backend
npm install
npm start

### ToDO
Automate certificate approval after it is created