
resource "aws_iam_role" "ssm_role" {
    name = "${var.project_name}-${var.environment}-ssm-role"

    assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    EOF
  
}

resource "aws_iam_role_policy_attachment" "ssm_role_policy_attachment" {
    role       = aws_iam_role.ssm_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm_instance_profile" {
    name = "${var.project_name}-${var.environment}-ssm-instance-profile"
    role = aws_iam_role.ssm_role.name
  
}