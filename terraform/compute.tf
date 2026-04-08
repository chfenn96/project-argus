# 1. Automatically find the latest Ubuntu 22.04 Image
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  owners = ["099720109477"] # Canonical's ID
}

# 2. Register the Key
resource "aws_key_pair" "argus_key" {
  key_name   = "${var.project_name}-key"
  public_key = file("${path.module}/../argus_key.pub")
}

# 3. Create the Server
resource "aws_instance" "control_plane" {
  ami           = data.aws_ami.ubuntu.id # Uses the search result
  instance_type = var.instance_type      # Uses the variable
  associate_public_ip_address = true 

  key_name      = aws_key_pair.argus_key.key_name
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  # Enforce IMDSv2 (Tokens Required)
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" 
    http_put_response_hop_limit = 1
  }

  # Encrypt the Root Disk
  # tfsec:ignore:aws-ec2-enable-at-rest-encryption (FinOps: Using default AWS key to avoid KMS costs)
  root_block_device {
    encrypted = true
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-control-plane"
  })
}