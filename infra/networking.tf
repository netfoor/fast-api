data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_subnet" "default" {
  for_each = toset(data.aws_subnets.default.ids)
  id       = each.value
}

data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_route_table" "main" {
  vpc_id = data.aws_vpc.default.id

  filter {
    name   = "association.main"
    values = ["true"]
  }
}


output "debug_vpc_info" {
  value = {
    vpc_id           = data.aws_vpc.default.id
    vpc_cidr         = data.aws_vpc.default.cidr_block
    subnet_ids       = data.aws_subnets.default.ids
    internet_gateway = data.aws_internet_gateway.default.id
    route_table_id   = data.aws_route_table.main.id
  }
}