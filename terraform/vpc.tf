# 1. The VPC - The "Fence" around our resources
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "argus-vpc"
  }
}

# 2. Public Subnet - For resources that need to be reachable from the internet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = false 
  availability_zone       = "us-east-1a"

  tags = {
    Name = "argus-public-subnet"
  }
}

# 3. Private Subnet - For our App/Database
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "argus-private-subnet"
  }
}

# 4. Internet Gateway - The "Door" to the internet for the VPC
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "argus-igw"
  }
}

# 5. Route Table for Public Subnet (Sends traffic to the Internet Gateway)
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0" # Representing all internet traffic
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "argus-public-rt"
  }
}

# 6. Associate Public Subnet with Public Route Table
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}