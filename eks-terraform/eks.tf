terraform {
  required_version = ">= 0.12.0"
}

module "eks" {
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  source                    = "terraform-aws-modules/eks/aws"
  cluster_name              = "alicek106-cluster"
  subnets                   = ["subnet-85b3afed", "subnet-effebea3"]
  manage_aws_auth           = true
  version                   = "~> 7.0.0"

  tags = {
    Owner = "alicek106"
  }

  vpc_id = "vpc-4f03e124"

  worker_groups_launch_template = [
    {
      name                 = "worker-group-template-1"
      instance_type        = "t2.small"
      autoscaling_enabled  = true
      asg_desired_capacity = 0
      asg_max_size         = 3
      asg_min_size         = 0
      public_ip            = true
      key_name             = "Docker Engine Test Instance"
      subnets              = ["subnet-85b3afed", "subnet-effebea3"]
      tags = [
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/taint/application", value = "alice:NoSchedule" },
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/label/application", value = "alice" },
      ]
      kubelet_extra_args = "--register-with-taints=application=alice:NoSchedule --node-labels=application=alice"
    },
    {
      name                 = "worker-group-template-2"
      instance_type        = "t2.medium"
      autoscaling_enabled  = true
      asg_desired_capacity = 0
      asg_max_size         = 3
      asg_min_size         = 0
      public_ip            = true
      key_name             = "Docker Engine Test Instance"
      subnets              = ["subnet-85b3afed"]
      tags = [
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/taint/application", value = "kingsley:NoSchedule" },
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/label/application", value = "kingsley" },
      ]
      kubelet_extra_args = "--register-with-taints=application=kingsley:NoSchedule --node-labels=application=kingsley"
    },
    {
      name                 = "worker-group-template-3"
      instance_type        = "t2.small"
      autoscaling_enabled  = true
      asg_desired_capacity = 0
      asg_max_size         = 3
      asg_min_size         = 0
      public_ip            = true
      key_name             = "Docker Engine Test Instance"
      subnets              = ["subnet-effebea3"]
      tags = [
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/taint/application", value = "kingsley:NoSchedule" },
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/label/application", value = "kingsley" },
      ]
      kubelet_extra_args = "--register-with-taints=application=kingsley:NoSchedule --node-labels=application=kingsley"
    },
    {
      name                 = "worker-group-template-4"
      instance_type        = "t2.medium"
      autoscaling_enabled  = true
      asg_desired_capacity = 0
      asg_max_size         = 3
      asg_min_size         = 0
      public_ip            = true
      key_name             = "Docker Engine Test Instance"
      subnets              = ["subnet-85b3afed"]
      tags = [
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/taint/application", value = "kingsley:NoSchedule" },
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/label/application", value = "kingsley" },
      ]
      kubelet_extra_args = "--register-with-taints=application=kingsley:NoSchedule --node-labels=application=kingsley"
    },
  ]

  worker_groups = [
    {
      name                 = "worker-group-configuration-1"
      autoscaling_enabled  = true
      instance_type        = "t2.small"
      asg_desired_capacity = 1
      asg_max_size         = 3
      asg_min_size         = 1
      key_name             = "Docker Engine Test Instance"
      subnets              = ["subnet-85b3afed", "subnet-effebea3"]
      tags = [
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/taint/application", value = "crpuz:NoSchedule" },
        { propagate_at_launch = true, key = "k8s.io/cluster-autoscaler/node-template/label/application", value = "crpuz" },
      ]

      kubelet_extra_args = "--register-with-taints=application=crpuz:NoSchedule --node-labels=application=crpuz"
    },
  ]
}
