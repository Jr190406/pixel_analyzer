from django.db import models
from django.contrib.auth.models import User  # If you're using Django auth
from django.core.validators import MinValueValidator, MaxValueValidator
import json

class UserProfile(models.Model):
    """Extended user profile with role-based access"""
    ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('business_owner', 'Business Owner'),
        ('super_admin', 'Super Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='regular')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_business_owner(self):
        return self.role == 'business_owner'
    
    def is_super_admin(self):
        return self.role == 'super_admin'
    
    def can_manage_pricing(self):
        return self.role in ['business_owner', 'super_admin']
    
    def can_view_all_users(self):
        return self.role == 'super_admin'

class CostSetting(models.Model):
    """Pricing rules that can be set by business owners"""
    PAPER_SIZE_CHOICES = [
        ('short', 'Letter (8.5" x 11")'),
        ('long', 'Legal (8.5" x 14")'),
        ('a4', 'A4 (210mm x 297mm)'),
        ('tabloid', 'Tabloid / Ledger (11" x 17")'),
        ('a3', 'A3 (297mm x 420mm)'),
        ('a3_plus', 'A3+ (329mm x 483mm)'),
        ('b4', 'B4 (250mm x 353mm)'),
        ('b3', 'B3 (353mm x 500mm)'),
        ('statement', 'Statement (5.5" x 8.5")'),
        ('executive', 'Executive (7.25" x 10.5")'),
    ]
    
    business_owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'userprofile__role__in': ['business_owner', 'super_admin']},
        help_text="Business owner who sets this pricing rule"
    )
    color = models.BooleanField(choices=[(True, 'Color'), (False, 'Black & White')])
    paper_size = models.CharField(
        max_length=10, 
        choices=PAPER_SIZE_CHOICES, 
        default='a4',
        help_text="Paper size for this pricing rule"
    )
    coverage_min = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    coverage_max = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_owner', 'color', 'paper_size', 'coverage_min', 'coverage_max')
        ordering = ['paper_size', 'coverage_min']

    def __str__(self):
        color_type = "Color" if self.color else "B&W"
        paper_display = self.get_paper_size_display()
        return f"{self.business_owner.username} - {color_type} {paper_display} {self.coverage_min}%-{self.coverage_max}%: ₱{self.cost}"

class DefaultPricingRule(models.Model):
    """Global default pricing rules - Configure system-wide pricing fallbacks"""
    PAPER_SIZE_CHOICES = [
        ('short', 'Letter (8.5" x 11")'),
        ('long', 'Legal (8.5" x 14")'),
        ('a4', 'A4 (210mm x 297mm)'),
        ('tabloid', 'Tabloid / Ledger (11" x 17")'),
        ('a3', 'A3 (297mm x 420mm)'),
        ('a3_plus', 'A3+ (329mm x 483mm)'),
        ('b4', 'B4 (250mm x 353mm)'),
        ('b3', 'B3 (353mm x 500mm)'),
        ('statement', 'Statement (5.5" x 8.5")'),
        ('executive', 'Executive (7.25" x 10.5")'),
    ]
    
    color = models.BooleanField(
        choices=[(True, 'Color'), (False, 'Black & White')],
        help_text="Whether this rule applies to color or black & white documents"
    )
    paper_size = models.CharField(
        max_length=10, 
        choices=PAPER_SIZE_CHOICES, 
        default='a4',
        help_text="Paper size for this pricing rule"
    )
    coverage_min = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Minimum coverage percentage (0-100)"
    )
    coverage_max = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Maximum coverage percentage (0-100)"
    )
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Cost in pesos for this coverage range"
    )
    reason = models.CharField(
        max_length=255,
        help_text="Description of this pricing rule (e.g., 'Light text coverage')"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this rule is currently active"
    )

    class Meta:
        unique_together = ('color', 'paper_size', 'coverage_min', 'coverage_max')
        ordering = ['paper_size', 'coverage_min']
        verbose_name = "Default Pricing Rule"
        verbose_name_plural = "Default Pricing Rules (System-wide)"

    def __str__(self):
        color_type = "Color" if self.color else "B&W"
        paper_display = self.get_paper_size_display()
        return f"Default {color_type} {paper_display} {self.coverage_min}%-{self.coverage_max}%: ₱{self.cost}"


class DocumentAnalysis(models.Model):
    """Store document analysis results for user history"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="User who uploaded the document"
    )
    document_name = models.CharField(
        max_length=255,
        help_text="Name of the uploaded document"
    )
    page_count = models.PositiveIntegerField(
        help_text="Total number of pages analyzed"
    )
    color_page_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of color pages"
    )
    bw_page_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of black & white pages"
    )
    overall_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total cost for the document"
    )
    analysis_result = models.JSONField(
        help_text="Detailed analysis results for each page"
    )
    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="File size in bytes"
    )
    file_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="File extension (pdf, jpg, png, etc.)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the analysis was performed"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Document Analysis"
        verbose_name_plural = "Document Analysis History"

    def __str__(self):
        return f"{self.document_name} - {self.user.username} (₱{self.overall_cost})"

    def get_analysis_summary(self):
        """Return a formatted summary of the analysis"""
        return f"{self.page_count} pages ({self.color_page_count} color, {self.bw_page_count} B&W)"

    def get_file_size_mb(self):
        """Return file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None


class PrintedDocument(models.Model):
    """Track documents that are actually printed for revenue calculation"""
    
    # Link to the original analysis
    analysis = models.ForeignKey(
        DocumentAnalysis,
        on_delete=models.CASCADE,
        related_name='printed_copies',
        help_text="Original document analysis"
    )
    
    # User who initiated the print (could be different from analyzer)
    printed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User who initiated the print job"
    )
    
    # Business owner whose pricing was used
    business_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='printed_revenue',
        limit_choices_to={'userprofile__role__in': ['business_owner', 'super_admin']},
        help_text="Business owner who earns revenue from this print"
    )
    
    # Print details
    paper_size = models.CharField(
        max_length=10,
        choices=[
            ('short', 'Letter (8.5" x 11")'),
            ('long', 'Legal (8.5" x 14")'),
            ('a4', 'A4 (210mm x 297mm)'),
            ('tabloid', 'Tabloid / Ledger (11" x 17")'),
            ('a3', 'A3 (297mm x 420mm)'),
            ('a3_plus', 'A3+ (329mm x 483mm)'),
            ('b4', 'B4 (250mm x 353mm)'),
            ('b3', 'B3 (353mm x 500mm)'),
            ('statement', 'Statement (5.5" x 8.5")'),
            ('executive', 'Executive (7.25" x 10.5")'),
        ],
        help_text="Paper size used for printing"
    )
    
    copies = models.PositiveIntegerField(
        default=1,
        help_text="Number of copies printed"
    )
    
    # Revenue calculation
    cost_per_copy = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Cost per single copy"
    )
    
    total_revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total revenue from this print job (cost_per_copy × copies)"
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('queued', 'Queued for Printing'),
            ('printing', 'Currently Printing'),
            ('completed', 'Print Completed'),
            ('cancelled', 'Print Cancelled'),
        ],
        default='queued',
        help_text="Current status of the print job"
    )
    
    # Timestamps
    queued_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the print job was queued"
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the print job was completed"
    )
    
    # Optional notes
    notes = models.TextField(
        blank=True,
        help_text="Optional notes about the print job"
    )

    class Meta:
        ordering = ['-queued_at']
        verbose_name = "Printed Document"
        verbose_name_plural = "Print History & Revenue"

    def __str__(self):
        status_display = self.get_status_display()
        return f"{self.analysis.document_name} - {self.copies}x copies - ₱{self.total_revenue} ({status_display})"

    def save(self, *args, **kwargs):
        # Auto-calculate total revenue
        if self.cost_per_copy and self.copies:
            self.total_revenue = self.cost_per_copy * self.copies
        super().save(*args, **kwargs)

    def get_revenue_summary(self):
        """Return formatted revenue summary"""
        return f"₱{self.total_revenue} ({self.copies} copies × ₱{self.cost_per_copy})"


class BusinessOwnerRequest(models.Model):
    """Model to store business owner access requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    VOLUME_CHOICES = [
        ('low', 'Low (1-100 documents/month)'),
        ('medium', 'Medium (100-500 documents/month)'),
        ('high', 'High (500+ documents/month)'),
    ]
    
    # User making the request
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_requests')
    
    # Business Information
    business_name = models.CharField(max_length=200, help_text="Official business name")
    business_type = models.CharField(max_length=100, help_text="Type of business (e.g., Print Shop)")
    business_address = models.TextField(help_text="Complete business address")
    business_phone = models.CharField(max_length=20, help_text="Business contact phone")
    business_email = models.EmailField(help_text="Business email address")
    
    # Registration Information (optional)
    business_registration_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="DTI/SEC/CDA registration number"
    )
    tax_id = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Tax Identification Number"
    )
    
    # Business Details
    years_in_operation = models.PositiveIntegerField(help_text="Years the business has been operating")
    monthly_volume = models.CharField(
        max_length=10, 
        choices=VOLUME_CHOICES,
        help_text="Expected monthly document volume"
    )
    business_description = models.TextField(help_text="Description of business and pricing needs")
    special_requirements = models.TextField(
        blank=True, 
        null=True,
        help_text="Any special pricing requirements"
    )
    
    # Request Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Admin notes about the request"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_business_requests',
        help_text="Admin who reviewed the request"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Business Owner Request"
        verbose_name_plural = "Business Owner Requests"
    
    def __str__(self):
        return f"{self.business_name} - {self.user.username} ({self.status})"
    
    def is_pending(self):
        return self.status == 'pending'
    
    def is_approved(self):
        return self.status == 'approved'
    
    def is_rejected(self):
        return self.status == 'rejected'

class RequestMessage(models.Model):
    """Messages between super admin and users regarding business owner requests"""
    request = models.ForeignKey(BusinessOwnerRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal_note = models.BooleanField(default=False, help_text="Internal notes only visible to super admin")
    created_at = models.DateTimeField(auto_now_add=True)
    read_by_user = models.BooleanField(default=False, help_text="Has the requesting user read this message")
    read_by_admin = models.BooleanField(default=False, help_text="Has the super admin read this message")
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Request Message"
        verbose_name_plural = "Request Messages"
    
    def __str__(self):
        sender_role = "Admin" if self.sender.userprofile.is_super_admin() else "User"
        message_type = " (Internal)" if self.is_internal_note else ""
        return f"{sender_role}: {self.message[:50]}...{message_type}"
    
    def mark_read_by_user(self):
        if not self.is_internal_note:
            self.read_by_user = True
            self.save()
    
    def mark_read_by_admin(self):
        self.read_by_admin = True
        self.save()

class RequestStatusChange(models.Model):
    """Track status changes and reasons for business owner requests"""
    request = models.ForeignKey(BusinessOwnerRequest, on_delete=models.CASCADE, related_name='status_changes')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True, help_text="Reason for status change")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Request Status Change"
        verbose_name_plural = "Request Status Changes"
    
    def __str__(self):
        return f"{self.request.business_name}: {self.old_status} → {self.new_status}"
