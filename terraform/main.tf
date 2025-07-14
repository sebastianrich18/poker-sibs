terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "poker" {
  name = "poker-cluster"
}

resource "aws_secretsmanager_secret" "db_url" {
  name = "poker-db-url"
}

resource "aws_secretsmanager_secret_version" "db_url" {
  secret_id     = aws_secretsmanager_secret.db_url.id
  secret_string = "postgresql://${var.db_username}:${var.db_password}@${aws_rds_cluster.poker.endpoint}/poker"
}

resource "aws_secretsmanager_secret" "api_secret" {
  name = "poker-api-secret"
}

resource "aws_secretsmanager_secret_version" "api_secret" {
  secret_id     = aws_secretsmanager_secret.api_secret.id
  secret_string = var.api_secret
}

resource "aws_rds_cluster" "poker" {
  engine            = "aurora-postgresql"
  master_username   = var.db_username
  master_password   = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.poker.name
  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot    = true
}

resource "aws_rds_cluster_instance" "poker" {
  count              = 1
  identifier         = "poker-${count.index}"
  cluster_identifier = aws_rds_cluster.poker.id
  instance_class     = "db.t3.micro"
  engine             = aws_rds_cluster.poker.engine
}

resource "aws_lb" "coordinator" {
  name               = "poker-coordinator"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]
  subnets            = data.aws_subnet_ids.default.ids
}

resource "aws_lb_target_group" "coordinator" {
  name     = "coordinator-tg"
  port     = 8000
  protocol = "HTTP"
  target_type = "ip"
  vpc_id   = data.aws_vpc.default.id
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.coordinator.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.coordinator.arn
  }
}

locals {
  db_url = aws_secretsmanager_secret_version.db_url.secret_string
}

resource "aws_iam_role" "ecs_task_execution" {
  name = "poker-task-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "coordinator" {
  family                   = "coordinator"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name  = "coordinator"
      image = var.coordinator_image
      portMappings = [{ containerPort = 8000 }]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.db_url.arn
        },
        {
          name      = "API_SECRET"
          valueFrom = aws_secretsmanager_secret.api_secret.arn
        }
      ]
    }
  ])
}

resource "aws_ecs_task_definition" "lobby" {
  family                   = "lobby"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  container_definitions    = jsonencode([
    {
      name  = "lobby"
      image = var.lobby_image
      portMappings = [{ containerPort = 8001 }]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.db_url.arn
        },
        {
          name      = "API_SECRET"
          valueFrom = aws_secretsmanager_secret.api_secret.arn
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "coordinator" {
  name            = "coordinator"
  cluster         = aws_ecs_cluster.poker.id
  task_definition = aws_ecs_task_definition.coordinator.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  load_balancer {
    target_group_arn = aws_lb_target_group.coordinator.arn
    container_name   = "coordinator"
    container_port   = 8000
  }
  network_configuration {
    subnets         = [data.aws_subnet_ids.default.ids[0]]
    assign_public_ip = true
    security_groups = [aws_security_group.ecs.id]
  }
}

resource "aws_ecs_service" "lobby" {
  name            = "lobby"
  cluster         = aws_ecs_cluster.poker.id
  task_definition = aws_ecs_task_definition.lobby.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = [data.aws_subnet_ids.default.ids[0]]
    assign_public_ip = true
    security_groups = [aws_security_group.ecs.id]
  }
}

resource "aws_security_group" "ecs" {
  name   = "poker-ecs"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  ingress {
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "lb" {
  name   = "poker-lb"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name   = "poker-db"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "default" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_db_subnet_group" "poker" {
  name       = "poker-db-subnets"
  subnet_ids = data.aws_subnet_ids.default.ids
}

resource "aws_appautoscaling_target" "coordinator" {
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.poker.name}/${aws_ecs_service.coordinator.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "coordinator" {
  name               = "coordinator-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.coordinator.resource_id
  scalable_dimension = aws_appautoscaling_target.coordinator.scalable_dimension
  service_namespace  = aws_appautoscaling_target.coordinator.service_namespace
  target_tracking_scaling_policy_configuration {
    target_value       = 50
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}

resource "aws_appautoscaling_target" "lobby" {
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.poker.name}/${aws_ecs_service.lobby.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "lobby" {
  name               = "lobby-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.lobby.resource_id
  scalable_dimension = aws_appautoscaling_target.lobby.scalable_dimension
  service_namespace  = aws_appautoscaling_target.lobby.service_namespace
  target_tracking_scaling_policy_configuration {
    target_value       = 50
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}

output "cluster_id" {
  value = aws_ecs_cluster.poker.id
}

output "coordinator_lb_dns" {
  value = aws_lb.coordinator.dns_name
}
