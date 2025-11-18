data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ami" "golden-ami-fastapi" {
  most_recent = true

  filter {
    name   = "name"
    values = ["golden-ami-fastapi-1763444433"]
  }

  owners = ["self"]
}

module "parameters" {
  source = "../../modules/parameters"

  SUPABASE_URL                = var.SUPABASE_URL
  SUPABASE_KEY                = var.SUPABASE_KEY
  POSTGRESQL_URL              = var.POSTGRESQL_URL
  SECRET_KEY                  = var.SECRET_KEY
  ALGORITHM                   = var.ALGORITHM
  ACCESS_TOKEN_EXPIRE_MINUTES = var.ACCESS_TOKEN_EXPIRE_MINUTES
}

module "sg_api" {
  source      = "../../modules/security-group"
  project     = "FastAPI Service"
  environment = "dev"
  description = "Security group for the FastAPI service"
  vpc_id      = data.aws_vpc.default.id
  ingress_rules = [
    {
      description = "Allow HTTP traffic"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "Allow HTTPS traffic"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
  tags = {
    "Name"        = "FastAPI Service"
    "Terraform"   = "true"
    "Environment" = "dev"
    "Owner"       = "Fortino Romero"
  }
}

module "ec2_api" {
  source               = "../../modules/ec2"
  project              = "FastAPI Service"
  environment          = "dev"
  ami_id               = data.aws_ami.golden-ami-fastapi.id
  instance_type        = "t2.micro"
  subnet_id            = data.aws_subnets.default.ids[0]
  iam_instance_profile = module.sg_api.iam_instance_profile

  security_groups = [module.sg_api.sg_id]

  disk_size = 20

  tags = {
    "Name"        = "FastAPI Service"
    "Terraform"   = "true"
    "Environment" = "dev"
    "Owner"       = "Fortino Romero"
  }
}