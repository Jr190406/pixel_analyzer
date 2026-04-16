#!/usr/bin/env python
"""
Test script to verify business owner pricing independence
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixel_cost_optimizer.settings')
django.setup()

from django.contrib.auth.models import User
from analyzer.models import UserProfile, CostSetting, DefaultPricingRule
from analyzer.views import get_pricing_for_user

def test_business_owner_pricing():
    """Test that business owners use their own pricing rules independently"""
    
    print("🧪 Testing Business Owner Pricing Independence")
    print("=" * 50)
    
    # Test case 1: Business owner with custom rules
    print("\n1. Testing business owner with custom pricing rules:")
    try:
        # Find a business owner with custom rules
        business_owner = User.objects.filter(
            userprofile__role='business_owner'
        ).first()
        
        if business_owner:
            custom_rules = CostSetting.objects.filter(
                business_owner=business_owner,
                is_active=True
            )
            
            if custom_rules.exists():
                print(f"   ✅ Found business owner: {business_owner.username}")
                print(f"   ✅ Custom rules count: {custom_rules.count()}")
                
                # Test pricing for color and black & white
                test_cases = [
                    (True, 15.0),   # Color, 15% coverage
                    (False, 25.0),  # B&W, 25% coverage
                ]
                
                for color, coverage in test_cases:
                    cost, reason = get_pricing_for_user(business_owner, color, coverage)
                    print(f"   📊 {color and 'Color' or 'B&W'} @ {coverage}% = ₱{cost} ({reason})")
            else:
                print(f"   ⚠️ Business owner {business_owner.username} has no custom rules")
        else:
            print("   ⚠️ No business owners found in database")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test case 2: Business owner without custom rules (should use default)
    print("\n2. Testing business owner without custom pricing rules:")
    try:
        # Create a test business owner without rules
        test_user, created = User.objects.get_or_create(
            username='test_business_owner',
            defaults={'email': 'test@example.com'}
        )
        
        profile, created = UserProfile.objects.get_or_create(
            user=test_user,
            defaults={'role': 'business_owner'}
        )
        
        # Ensure no custom rules
        CostSetting.objects.filter(business_owner=test_user).delete()
        
        # Test pricing (should use default)
        cost, reason = get_pricing_for_user(test_user, True, 20.0)
        print(f"   📊 Color @ 20% = ₱{cost} ({reason})")
        
        if "Default pricing" in reason:
            print("   ✅ Correctly using default pricing when no custom rules exist")
        else:
            print("   ⚠️ May not be using default pricing as expected")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test case 3: Regular user (should always use default)
    print("\n3. Testing regular user pricing:")
    try:
        regular_user = User.objects.filter(
            userprofile__role='regular'
        ).first()
        
        if regular_user:
            cost, reason = get_pricing_for_user(regular_user, True, 30.0)
            print(f"   📊 Regular user Color @ 30% = ₱{cost} ({reason})")
            print("   ✅ Regular users should always use default/admin pricing")
        else:
            print("   ⚠️ No regular users found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_business_owner_pricing()
