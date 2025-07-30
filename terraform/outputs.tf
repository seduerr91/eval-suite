# --- Outputs ---
# Defines the output variables that can be easily queried after deployment.

output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer."
  value       = aws_lb.main.dns_name
}

output "route53_name_servers" {
  description = "The name servers for the Route 53 hosted zone."
  value       = aws_route53_zone.main.name_servers
}
