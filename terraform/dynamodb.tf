resource "aws_dynamodb_table" "http_crud_tutorial_users_table" {
  name         = "http-crud-tutorial-users"
  hash_key     = "id"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "id"
    type = "S"
  }
}