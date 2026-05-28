# Resource block configuring a Managed Amazon Relational Database Service (RDS)
resource "aws_db_instance" "analytical_warehouse" {
  allocated_storage    = 5000 # 5 Terabytes of high-speed solid-state memory
  engine               = "mysql"
  engine_version       = "8.0"
  
  # FINANCIAL OVERHEAD FLAW: db.m5.24xlarge provides 96 CPUs and 384 GB of RAM
  # This single server instance costs roughly $3,500 every single month!
  instance_class       = "db.m5.24xlarge"
  
  db_name              = "analytics_prod"
  username             = "admin"
  password             = "HighlySecureProductionPassword2026!"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
}