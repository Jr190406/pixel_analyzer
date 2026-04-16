from django.core.management.base import BaseCommand
from analyzer.models import DefaultPricingRule

class Command(BaseCommand):
    help = 'Create default pricing rules'

    def handle(self, *args, **options):
        # Clear existing default rules
        DefaultPricingRule.objects.all().delete()
        
        # Create detailed default pricing rules
        default_rules = [
            # Black & White pricing tiers
            {
                'color': False,
                'coverage_min': 0.0,
                'coverage_max': 9.99,
                'cost': 0.50,
                'reason': 'Minimal B&W printing (text only)'
            },
            {
                'color': False,
                'coverage_min': 10.0,
                'coverage_max': 15.0,
                'cost': 1.00,
                'reason': 'B&W with small graphics/logo (10-15%)'
            },
            {
                'color': False,
                'coverage_min': 15.01,
                'coverage_max': 19.99,
                'cost': 1.25,
                'reason': 'B&W moderate content (15-20%)'
            },
            {
                'color': False,
                'coverage_min': 20.0,
                'coverage_max': 30.0,
                'cost': 1.50,
                'reason': 'B&W medium coverage (20-30%)'
            },
            {
                'color': False,
                'coverage_min': 30.01,
                'coverage_max': 49.99,
                'cost': 1.75,
                'reason': 'B&W high content (30-50%)'
            },
            {
                'color': False,
                'coverage_min': 50.0,
                'coverage_max': 59.99,
                'cost': 2.00,
                'reason': 'B&W half page coverage (50%)'
            },
            {
                'color': False,
                'coverage_min': 60.0,
                'coverage_max': 70.0,
                'cost': 2.25,
                'reason': 'B&W heavy coverage (60-70%)'
            },
            {
                'color': False,
                'coverage_min': 70.01,
                'coverage_max': 99.99,
                'cost': 2.50,
                'reason': 'B&W very heavy coverage (70-99%)'
            },
            {
                'color': False,
                'coverage_min': 100.0,
                'coverage_max': 100.0,
                'cost': 3.00,
                'reason': 'B&W full page coverage (100%)'
            },
            
            # Color printing tiers
            {
                'color': True,
                'coverage_min': 0.0,
                'coverage_max': 9.99,
                'cost': 1.00,
                'reason': 'Minimal color printing (text with highlights)'
            },
            {
                'color': True,
                'coverage_min': 10.0,
                'coverage_max': 15.0,
                'cost': 2.00,
                'reason': 'Color with logo/small graphics (10-15%)'
            },
            {
                'color': True,
                'coverage_min': 15.01,
                'coverage_max': 19.99,
                'cost': 2.50,
                'reason': 'Color moderate content (15-20%)'
            },
            {
                'color': True,
                'coverage_min': 20.0,
                'coverage_max': 30.0,
                'cost': 3.50,
                'reason': 'Color medium coverage (20-30%)'
            },
            {
                'color': True,
                'coverage_min': 30.01,
                'coverage_max': 49.99,
                'cost': 4.50,
                'reason': 'Color high content (30-50%)'
            },
            {
                'color': True,
                'coverage_min': 50.0,
                'coverage_max': 59.99,
                'cost': 5.50,
                'reason': 'Color half page coverage (50%)'
            },
            {
                'color': True,
                'coverage_min': 60.0,
                'coverage_max': 70.0,
                'cost': 6.50,
                'reason': 'Color heavy coverage (60-70%)'
            },
            {
                'color': True,
                'coverage_min': 70.01,
                'coverage_max': 99.99,
                'cost': 7.50,
                'reason': 'Color very heavy coverage (70-99%)'
            },
            {
                'color': True,
                'coverage_min': 100.0,
                'coverage_max': 100.0,
                'cost': 10.00,
                'reason': 'Color full page coverage (100%)'
            },
        ]
        
        for rule_data in default_rules:
            DefaultPricingRule.objects.create(**rule_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created rule: {rule_data["reason"]} - ${rule_data["cost"]}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(default_rules)} default pricing rules')
        )
