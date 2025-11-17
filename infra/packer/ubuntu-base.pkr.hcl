packer {
  required_version = ">= 1.8.0"

  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = ">= 1.2.8"
    }
  }
}

##################################################
# VARIABLES
##################################################

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

# Optional: pin an AMI (CI/CD can override this)
variable "base_ami" {
  type        = string
  default     = ""
  description = "If empty, use dynamic Ubuntu 22.04 lookup"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "ami_base_name" {
  type    = string
  default = "golden-ami-fastapi"
}

variable "enable_dynamic_lookup" {
  type        = bool
  default     = true
  description = "Set false to use base_ami directly"
}

##################################################
# AMAZON SOURCE TEMPLATE
##################################################

source "amazon-ebs" "ubuntu" {

  region        = var.aws_region
  instance_type = var.instance_type
  ssh_username  = "ubuntu"

  ##################################################
  # AMI BASE SELECTION (dynamic or pinned)
  ##################################################
  source_ami = var.enable_dynamic_lookup ? null : var.base_ami

  dynamic "source_ami_filter" {
    for_each = var.enable_dynamic_lookup ? [1] : []
    content {
      filters = {
        name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
        root-device-type    = "ebs"
        virtualization-type = "hvm"
      }
      owners      = ["099720109477"]
      most_recent = true
    }
  }

  ##################################################
  # AMI NAMING
  ##################################################
  ami_name = "${var.ami_base_name}-{{timestamp}}"

  ##################################################
  # TAGGING
  ##################################################
  ami_description = "Golden AMI for FastAPI application with Docker + SystemD services installed"

  tags = {
    Name       = var.ami_base_name
    Build-Date = "{{timestamp}}"
    Managed-By = "Packer"
    OS         = "Ubuntu 22.04"
  }

  snapshot_tags = {
    Name       = "${var.ami_base_name}-snapshot"
    Managed-By = "Packer"
  }

  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 10
    volume_type           = "gp3"
    delete_on_termination = true
  }
}

##################################################
# BUILD BLOCK
##################################################

build {
  name    = "golden-ami-fastapi"
  sources = ["source.amazon-ebs.ubuntu"]

  ##################################################
  # PRE-BUILD HOOKS
  ##################################################
  provisioner "shell" {
    inline = [
      "echo '[PRE] Starting build…'",
      "sudo apt-get update -y"
    ]
  }

  ##################################################
  # MAIN BUILD SCRIPTS
  ##################################################
  provisioner "shell" {
    script = "scripts/install_docker.sh"
  }

  provisioner "shell" {
    script = "scripts/setup_systemd.sh"
  }

  ##################################################
  # CLEANUP
  ##################################################
  provisioner "shell" {
    script = "scripts/cleanup.sh"
  }

  ##################################################
  # POST-BUILD HOOKS
  ##################################################
  post-processor "shell-local" {
    inline = [
      "echo '[POST] AMI Build Completed!'"
    ]
  }
}
