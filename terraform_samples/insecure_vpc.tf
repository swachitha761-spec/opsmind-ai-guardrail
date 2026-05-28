# Resource block defining an AWS Network Firewall Security Group
resource "aws_security_group" "production_firewall" {
  name        = "production-frontend-sg"
  description = "Security firewall configuration for public web entry"
  vpc_id      = "vpc-0123456789abcdef0"

  # INGRESS RULE: Controls traffic coming into the network
  ingress {
    description = "Allow SSH management access globally"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    
    # CRITICAL SEVERITY LAW: 0.0.0.0/0 means ANY computer on the public internet can attempt to hack this port
    cidr_blocks = ["0.0.0.0/0"] 
  }

  # EGRESS RULE: Controls traffic leaving the network
  egress {
    description = "Allow unrestricted outbound data transfer"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}