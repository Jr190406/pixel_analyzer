from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class BusinessOwnerRequest(models.Model):
    """Model for business owner access requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    # User Information
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Business Information
    business_name = models.CharField(max_length=200, help_text="Official business name")
    business_type = models.CharField(max_length=100, help_text="Type of business (e.g., Print Shop, Copy Center)")
    business_address = models.TextField(help_text="Complete business address")
    business_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number')]
    )
    business_email = models.EmailField(help_text="Business email address")
    
    # Registration/License Information
    business_registration_number = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Business registration or license number"
    )
    tax_id = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Tax ID or TIN number"
    )
    
    # Business Details
    years_in_operation = models.PositiveIntegerField(help_text="How many years in business")
    monthly_volume = models.CharField(
        max_length=50,
        choices=[
            ('low', 'Low (1-100 documents/month)'),
            ('medium', 'Medium (100-500 documents/month)'),
            ('high', 'High (500+ documents/month)'),
        ],
        help_text="Expected monthly document volume"
    )
    
    # Additional Information
    business_description = models.TextField(
        help_text="Brief description of your business and why you need pricing control"
    )
    special_requirements = models.TextField(
        blank=True,
        help_text="Any special pricing requirements or considerations"
    )
    
    # Request Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_requests'
    )
    admin_notes = models.TextField(blank=True, help_text="Internal admin notes")
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection")
    
    class Meta:
        verbose_name = "Business Owner Request"
        verbose_name_plural = "Business Owner Requests"
        ordering = ['-request_date']
    
    def __str__(self):
        return f"{self.business_name} - {self.user.username} ({self.get_status_display()})"


class BusinessSubscription(models.Model):
    """Model for business subscription management"""
    PLAN_CHOICES = [
        ('basic', 'Basic Plan - ₱500/month'),
        ('premium', 'Premium Plan - ₱1000/month'),
        ('enterprise', 'Enterprise Plan - ₱2000/month'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    
    # Subscription Dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    
    # Payment Information
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Features
    max_pricing_rules = models.PositiveIntegerField(default=10)
    max_monthly_documents = models.PositiveIntegerField(default=1000)
    priority_support = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Business Subscription"
        verbose_name_plural = "Business Subscriptions"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} ({self.get_status_display()})"
    
    def is_active(self):
        return self.status == 'active'
    
    def days_until_expiry(self):
        from django.utils import timezone
        if self.end_date:
            return (self.end_date - timezone.now()).days
        return 0
