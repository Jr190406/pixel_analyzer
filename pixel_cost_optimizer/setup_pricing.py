#!/usr/bin/env python
"""
Setup default pricing rules for regular users
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\hello\\OneDrive\\Documents\\GeraldezTesting\\pixel_cost_optimizer')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixel_cost_optimizer.settings')
django.setup()

# Now import Django modules
from analyzer.models import DefaultPricingRule

def setup_default_pricing():
    """Create default pricing rules if they don't exist"""
    print("Setting up default pricing rules...")
    
    # Check existing rules
    existing_rules = DefaultPricingRule.objects.all()
    print(f"Found {existing_rules.count()} existing default pricing rules")
    
    if existing_rules.count() == 0:
        print("Creating default pricing rules...")
        
        # Create basic pricing rules for Color documents
        DefaultPricingRule.objects.create(
            color=True,
            coverage_min=0.0,
            coverage_max=25.0,
            cost=2.00,
            reason="Color document - Light coverage (0-25%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=True,
            coverage_min=25.01,
            coverage_max=50.0,
            cost=3.00,
            reason="Color document - Medium coverage (25-50%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=True,
            coverage_min=50.01,
            coverage_max=75.0,
            cost=4.00,
            reason="Color document - Heavy coverage (50-75%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=True,
            coverage_min=75.01,
            coverage_max=100.0,
            cost=5.00,
            reason="Color document - Full coverage (75-100%)",
            is_active=True
        )
        
        # Create basic pricing rules for B&W documents
        DefaultPricingRule.objects.create(
            color=False,
            coverage_min=0.0,
            coverage_max=25.0,
            cost=1.00,
            reason="B&W document - Light coverage (0-25%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=False,
            coverage_min=25.01,
            coverage_max=50.0,
            cost=1.50,
            reason="B&W document - Medium coverage (25-50%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=False,
            coverage_min=50.01,
            coverage_max=75.0,
            cost=2.00,
            reason="B&W document - Heavy coverage (50-75%)",
            is_active=True
        )
        
        DefaultPricingRule.objects.create(
            color=False,
            coverage_min=75.01,
            coverage_max=100.0,
            cost=2.50,
            reason="B&W document - Full coverage (75-100%)",
            is_active=True
        )
        
        print("✅ Created 8 default pricing rules")
    else:
        print("Default pricing rules already exist:")
        for rule in existing_rules:
            print(f"  - {rule}")

if __name__ == "__main__":
    setup_default_pricing()
