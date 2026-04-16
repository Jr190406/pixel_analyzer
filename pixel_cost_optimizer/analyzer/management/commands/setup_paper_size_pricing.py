from django.core.management.base import BaseCommand
from analyzer.models import DefaultPricingRule

class Command(BaseCommand):
    help = 'Setup default pricing rules with paper sizes'

    def handle(self, *args, **options):
        # Clear existing default pricing rules
        DefaultPricingRule.objects.all().delete()
        self.stdout.write("Cleared existing default pricing rules")
        
        # Create comprehensive pricing for all paper sizes
        paper_sizes = ['short', 'long', 'a4']
        
        for paper_size in paper_sizes:
            # B&W pricing for different coverage ranges
            bw_rules = [
                (0, 10, 2.00, "Light text/minimal content"),
                (10, 25, 3.50, "Light to medium text coverage"),
                (25, 50, 5.00, "Medium content coverage"),
                (50, 75, 7.50, "Heavy content coverage"),
                (75, 100, 10.00, "Very heavy to full coverage")
            ]
            
            # Color pricing (higher rates)
            color_rules = [
                (0, 10, 5.00, "Light color elements"),
                (10, 25, 8.00, "Light to medium color coverage"),
                (25, 50, 12.00, "Medium color coverage"),
                (50, 75, 18.00, "Heavy color coverage"),
                (75, 100, 25.00, "Very heavy to full color coverage")
            ]
            
            # Create B&W rules
            for min_cov, max_cov, cost, reason in bw_rules:
                DefaultPricingRule.objects.create(
                    color=False,
                    paper_size=paper_size,
                    coverage_min=min_cov,
                    coverage_max=max_cov,
                    cost=cost,
                    reason=f"{reason} ({paper_size.upper()} paper)",
                    is_active=True
                )
            
            # Create Color rules
            for min_cov, max_cov, cost, reason in color_rules:
                DefaultPricingRule.objects.create(
                    color=True,
                    paper_size=paper_size,
                    coverage_min=min_cov,
                    coverage_max=max_cov,
                    cost=cost,
                    reason=f"{reason} ({paper_size.upper()} paper)",
                    is_active=True
                )
        
        total_rules = DefaultPricingRule.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {total_rules} default pricing rules with paper sizes!')
        )
        
        # Show breakdown
        for paper_size in paper_sizes:
            bw_count = DefaultPricingRule.objects.filter(paper_size=paper_size, color=False).count()
            color_count = DefaultPricingRule.objects.filter(paper_size=paper_size, color=True).count()
            self.stdout.write(f"  {paper_size.upper()}: {bw_count} B&W + {color_count} Color = {bw_count + color_count} rules")