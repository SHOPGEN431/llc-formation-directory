from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime
import json

app = Flask(__name__)

# Global variables
llc_data = None

# Static states data
states_data = {
    'alabama': {'name': 'Alabama', 'abbr': 'AL', 'formation_fee': 200, 'annual_fee': 100},
    'alaska': {'name': 'Alaska', 'abbr': 'AK', 'formation_fee': 250, 'annual_fee': 100},
    'arizona': {'name': 'Arizona', 'abbr': 'AZ', 'formation_fee': 50, 'annual_fee': 0},
    'arkansas': {'name': 'Arkansas', 'abbr': 'AR', 'formation_fee': 45, 'annual_fee': 150},
    'california': {'name': 'California', 'abbr': 'CA', 'formation_fee': 70, 'annual_fee': 800},
    'colorado': {'name': 'Colorado', 'abbr': 'CO', 'formation_fee': 50, 'annual_fee': 10},
    'connecticut': {'name': 'Connecticut', 'abbr': 'CT', 'formation_fee': 120, 'annual_fee': 20},
    'delaware': {'name': 'Delaware', 'abbr': 'DE', 'formation_fee': 90, 'annual_fee': 300},
    'florida': {'name': 'Florida', 'abbr': 'FL', 'formation_fee': 125, 'annual_fee': 138.75},
    'georgia': {'name': 'Georgia', 'abbr': 'GA', 'formation_fee': 100, 'annual_fee': 50},
    'hawaii': {'name': 'Hawaii', 'abbr': 'HI', 'formation_fee': 50, 'annual_fee': 15},
    'idaho': {'name': 'Idaho', 'abbr': 'ID', 'formation_fee': 100, 'annual_fee': 0},
    'illinois': {'name': 'Illinois', 'abbr': 'IL', 'formation_fee': 150, 'annual_fee': 75},
    'indiana': {'name': 'Indiana', 'abbr': 'IN', 'formation_fee': 90, 'annual_fee': 30},
    'iowa': {'name': 'Iowa', 'abbr': 'IA', 'formation_fee': 50, 'annual_fee': 30},
    'kansas': {'name': 'Kansas', 'abbr': 'KS', 'formation_fee': 165, 'annual_fee': 55},
    'kentucky': {'name': 'Kentucky', 'abbr': 'KY', 'formation_fee': 40, 'annual_fee': 15},
    'louisiana': {'name': 'Louisiana', 'abbr': 'LA', 'formation_fee': 100, 'annual_fee': 35},
    'maine': {'name': 'Maine', 'abbr': 'ME', 'formation_fee': 175, 'annual_fee': 85},
    'maryland': {'name': 'Maryland', 'abbr': 'MD', 'formation_fee': 100, 'annual_fee': 300},
    'massachusetts': {'name': 'Massachusetts', 'abbr': 'MA', 'formation_fee': 500, 'annual_fee': 500},
    'michigan': {'name': 'Michigan', 'abbr': 'MI', 'formation_fee': 50, 'annual_fee': 25},
    'minnesota': {'name': 'Minnesota', 'abbr': 'MN', 'formation_fee': 155, 'annual_fee': 25},
    'mississippi': {'name': 'Mississippi', 'abbr': 'MS', 'formation_fee': 50, 'annual_fee': 25},
    'missouri': {'name': 'Missouri', 'abbr': 'MO', 'formation_fee': 50, 'annual_fee': 0},
    'montana': {'name': 'Montana', 'abbr': 'MT', 'formation_fee': 70, 'annual_fee': 20},
    'nebraska': {'name': 'Nebraska', 'abbr': 'NE', 'formation_fee': 100, 'annual_fee': 10},
    'nevada': {'name': 'Nevada', 'abbr': 'NV', 'formation_fee': 75, 'annual_fee': 325},
    'new-hampshire': {'name': 'New Hampshire', 'abbr': 'NH', 'formation_fee': 100, 'annual_fee': 100},
    'new-jersey': {'name': 'New Jersey', 'abbr': 'NJ', 'formation_fee': 125, 'annual_fee': 75},
    'new-mexico': {'name': 'New Mexico', 'abbr': 'NM', 'formation_fee': 50, 'annual_fee': 0},
    'new-york': {'name': 'New York', 'abbr': 'NY', 'formation_fee': 200, 'annual_fee': 9},
    'north-carolina': {'name': 'North Carolina', 'abbr': 'NC', 'formation_fee': 125, 'annual_fee': 200},
    'north-dakota': {'name': 'North Dakota', 'abbr': 'ND', 'formation_fee': 135, 'annual_fee': 50},
    'ohio': {'name': 'Ohio', 'abbr': 'OH', 'formation_fee': 99, 'annual_fee': 0},
    'oklahoma': {'name': 'Oklahoma', 'abbr': 'OK', 'formation_fee': 100, 'annual_fee': 25},
    'oregon': {'name': 'Oregon', 'abbr': 'OR', 'formation_fee': 100, 'annual_fee': 100},
    'pennsylvania': {'name': 'Pennsylvania', 'abbr': 'PA', 'formation_fee': 125, 'annual_fee': 70},
    'rhode-island': {'name': 'Rhode Island', 'abbr': 'RI', 'formation_fee': 150, 'annual_fee': 50},
    'south-carolina': {'name': 'South Carolina', 'abbr': 'SC', 'formation_fee': 110, 'annual_fee': 0},
    'south-dakota': {'name': 'South Dakota', 'abbr': 'SD', 'formation_fee': 150, 'annual_fee': 50},
    'tennessee': {'name': 'Tennessee', 'abbr': 'TN', 'formation_fee': 300, 'annual_fee': 300},
    'texas': {'name': 'Texas', 'abbr': 'TX', 'formation_fee': 300, 'annual_fee': 0},
    'utah': {'name': 'Utah', 'abbr': 'UT', 'formation_fee': 70, 'annual_fee': 20},
    'vermont': {'name': 'Vermont', 'abbr': 'VT', 'formation_fee': 125, 'annual_fee': 35},
    'virginia': {'name': 'Virginia', 'abbr': 'VA', 'formation_fee': 100, 'annual_fee': 50},
    'washington': {'name': 'Washington', 'abbr': 'WA', 'formation_fee': 200, 'annual_fee': 60},
    'west-virginia': {'name': 'West Virginia', 'abbr': 'WV', 'formation_fee': 100, 'annual_fee': 25},
    'wisconsin': {'name': 'Wisconsin', 'abbr': 'WI', 'formation_fee': 130, 'annual_fee': 25},
    'wyoming': {'name': 'Wyoming', 'abbr': 'WY', 'formation_fee': 100, 'annual_fee': 50}
}

# Sample business data for demonstration
sample_businesses = [
    {'name': 'Northwest Registered Agent', 'city': 'New York', 'state': 'NY', 'rating': 4.8, 'reviews': 15000},
    {'name': 'LegalZoom', 'city': 'Los Angeles', 'state': 'CA', 'rating': 4.5, 'reviews': 12000},
    {'name': 'Rocket Lawyer', 'city': 'Chicago', 'state': 'IL', 'rating': 4.3, 'reviews': 8000},
    {'name': 'Incfile', 'city': 'Houston', 'state': 'TX', 'rating': 4.6, 'reviews': 10000},
    {'name': 'ZenBusiness', 'city': 'Austin', 'state': 'TX', 'rating': 4.7, 'reviews': 9000}
]

# Context processor to make states_data available in all templates
@app.context_processor
def inject_states_data():
    return dict(states_data=states_data)

# Context processor to make top cities available in all templates
@app.context_processor
def inject_top_cities():
    # Return sample top cities
    top_cities = [
        {'city': 'New York', 'count': 150, 'state': 'NY', 'state_slug': 'new-york', 'city_slug': 'new-york'},
        {'city': 'Los Angeles', 'count': 120, 'state': 'CA', 'state_slug': 'california', 'city_slug': 'los-angeles'},
        {'city': 'Chicago', 'count': 100, 'state': 'IL', 'state_slug': 'illinois', 'city_slug': 'chicago'},
        {'city': 'Houston', 'count': 90, 'state': 'TX', 'state_slug': 'texas', 'city_slug': 'houston'},
        {'city': 'Phoenix', 'count': 80, 'state': 'AZ', 'state_slug': 'arizona', 'city_slug': 'phoenix'}
    ]
    return dict(top_cities=top_cities)

def generate_seo_url(text):
    """Generate SEO-friendly URL from text"""
    if pd.isna(text) or text == '':
        return ''
    return text.lower().replace(' ', '-').replace(',', '').replace('.', '').replace("'", '').replace('"', '')

def get_structured_data(business_type="Service", name="llcdirectory.org", description="Find local businesses"):
    """Generate structured data for SEO"""
    return {
        "@context": "https://schema.org",
        "@type": business_type,
        "name": name,
        "description": description,
        "provider": {
            "@type": "Organization",
            "name": "llcdirectory.org"
        }
    }

@app.route('/test')
def test():
    """Simple test route to verify the app is working"""
    return "LLC Formation Directory is working!"

@app.route('/')
def index():
    """Homepage - LLC Formation Services Directory"""
    title = "LLC Formation Services Directory - Find Local Business Formation Providers"
    meta_description = "Find local LLC formation services with reviews and contact information. Browse by city, state, or search for business formation providers near you."
    
    # Get popular cities (sample data)
    popular_cities = [
        {'city': 'New York', 'count': 150, 'state': 'NY', 'state_slug': 'new-york', 'city_slug': 'new-york'},
        {'city': 'Los Angeles', 'count': 120, 'state': 'CA', 'state_slug': 'california', 'city_slug': 'los-angeles'},
        {'city': 'Chicago', 'count': 100, 'state': 'IL', 'state_slug': 'illinois', 'city_slug': 'chicago'},
        {'city': 'Houston', 'count': 90, 'state': 'TX', 'state_slug': 'texas', 'city_slug': 'houston'},
        {'city': 'Phoenix', 'count': 80, 'state': 'AZ', 'state_slug': 'arizona', 'city_slug': 'phoenix'}
    ]
    
    return render_template('index.html',
                         title=title,
                         meta_description=meta_description,
                         cities_by_state={},
                         popular_cities=popular_cities,
                         structured_data=get_structured_data("WebSite", "LLC Formation Services Directory", "Find local LLC formation services in your area"))

@app.route('/city/<state_slug>/<city_slug>')
@app.route('/city/<state_slug>/<city_slug>/page/<int:page>')
def city_directory(state_slug, city_slug, page=1):
    """City-specific business directory page with pagination"""
    if state_slug not in states_data:
        return "State not found", 404
    
    state_info = states_data[state_slug]
    per_page = 5
    
    # Filter sample businesses for this city/state
    city_businesses = []
    for business in sample_businesses:
        if (business['state'].lower() == state_info['abbr'].lower() and 
            business['city'].lower().replace(' ', '-') == city_slug.lower()):
            city_businesses.append(business)
    
    # If no businesses found, return sample data
    if not city_businesses:
        city_businesses = sample_businesses[:3]
    
    # Calculate pagination
    total_businesses = len(city_businesses)
    total_pages = (total_businesses + per_page - 1) // per_page
    
    # Ensure page is within valid range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    # Get businesses for current page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    current_page_businesses = city_businesses[start_idx:end_idx]
    
    city_name = city_slug.replace('-', ' ').title()
    title = f"Best LLC Formation Services in {city_name}, {state_info['abbr']} (2025 Reviews)"
    meta_description = f"Find the top-rated LLC formation services in {city_name}. Get professional help with business registration, legal services, and everything you need to start your LLC in {city_name}."
    
    return render_template('city_directory.html',
                         state=state_info,
                         city_name=city_name,
                         city_slug=city_slug,
                         businesses=current_page_businesses,
                         all_businesses=city_businesses,
                         state_businesses=sample_businesses,
                         current_page=page,
                         total_pages=total_pages,
                         total_businesses=total_businesses,
                         per_page=per_page,
                         businesses_4_plus=len([b for b in city_businesses if b.get('rating', 0) >= 4.0]),
                         businesses_3_plus=len([b for b in city_businesses if b.get('rating', 0) >= 3.0]),
                         businesses_with_reviews=len([b for b in city_businesses if b.get('rating', 0) > 0]),
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_city_structured_data(state_info, city_name))

def get_city_structured_data(state_info, city_name):
    """Generate structured data for city pages"""
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"Business Directory - {city_name}, {state_info['name']}",
        "description": f"Find local businesses in {city_name}, {state_info['name']}",
        "mainEntity": {
            "@type": "City",
            "name": city_name,
            "addressRegion": state_info['name'],
            "addressCountry": "US"
        }
    }

@app.route('/state/<state_slug>')
def state_directory(state_slug):
    """State-specific LLC formation services directory page"""
    if state_slug not in states_data:
        return "State not found", 404
    
    state_info = states_data[state_slug]
    
    # Filter sample businesses for this state
    state_businesses = []
    for business in sample_businesses:
        if business['state'].lower() == state_info['abbr'].lower():
            state_businesses.append(business)
    
    # If no businesses found, return sample data
    if not state_businesses:
        state_businesses = sample_businesses[:3]
    
    # Get cities in this state (sample data)
    cities = [
        {'city': 'New York', 'count': 150, 'slug': 'new-york'},
        {'city': 'Los Angeles', 'count': 120, 'slug': 'los-angeles'},
        {'city': 'Chicago', 'count': 100, 'slug': 'chicago'}
    ]
    
    title = f"LLC Formation Services in {state_info['name']} (2025 Directory)"
    meta_description = f"Find the best LLC formation services in {state_info['name']}. Get professional help with business registration, legal services, and everything you need to start your LLC in {state_info['name']}."
    
    return render_template('state_directory.html',
                         state=state_info,
                         businesses=state_businesses,
                         cities=cities,
                         total_businesses=len(state_businesses),
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_state_structured_data(state_info))

def get_state_structured_data(state_info):
    """Generate structured data for state pages"""
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"Business Directory - {state_info['name']}",
        "description": f"Find local businesses in {state_info['name']}",
        "mainEntity": {
            "@type": "State",
            "name": state_info['name'],
            "addressCountry": "US"
        }
    }

@app.route('/about')
def about():
    """About page"""
    title = "About llcdirectory.org"
    meta_description = "Learn about llcdirectory.org - your comprehensive resource for LLC formation services, guides, and tools."
    
    return render_template('about.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/privacy-policy')
def privacy_policy():
    """Privacy Policy page"""
    title = "Privacy Policy - Rigma Marketing LLC"
    meta_description = "Privacy Policy for Rigma Marketing LLC. Learn how we collect, use, and protect your information, including affiliate tracking disclosure."
    
    return render_template('privacy_policy.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/terms-conditions')
def terms_conditions():
    """Terms and Conditions page"""
    title = "Terms and Conditions - Rigma Marketing LLC"
    meta_description = "Terms and Conditions for Rigma Marketing LLC. Read our terms of service, usage policies, and legal agreements for using our website."
    
    return render_template('terms_conditions.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/contact')
def contact():
    """Contact page"""
    title = "Contact Us - Rigma Marketing LLC"
    meta_description = "Contact Rigma Marketing LLC for questions about LLC formation services, business tools, and our directory. Get in touch with our expert team."
    
    return render_template('contact.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/calculators')
def calculators():
    """Calculators landing page"""
    title = "Business Calculators - LLC Formation Tools"
    meta_description = "Free business calculators for LLC formation. Calculate break-even analysis, ROI, and equity splits for your business."
    
    return render_template('calculators.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/resources')
def resources():
    """Resources landing page"""
    title = "Business Resources - LLC Formation Tools & Guides"
    meta_description = "Comprehensive business resources for LLC formation. Access calculators, quizzes, checklists, and expert guidance to start your business."
    
    return render_template('resources.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/business-structure-quiz')
def business_structure_quiz():
    """Business structure quiz"""
    title = "Business Structure Quiz - Find Your Perfect Business Type"
    meta_description = "Take our business structure quiz to determine if an LLC, S-Corp, or C-Corp is right for your business goals and circumstances."
    
    return render_template('business_structure_quiz.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/llc-cost-calculator')
def llc_cost_calculator():
    """LLC formation cost calculator"""
    title = "LLC Formation Cost Calculator - State-by-State Pricing"
    meta_description = "Calculate the total cost of forming an LLC in your state. Compare service providers and get accurate pricing for your business formation."
    
    return render_template('llc_cost_calculator.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/foreign-qualification-checklist')
def foreign_qualification_checklist():
    """Foreign qualification checklist"""
    title = "Foreign Qualification Checklist - Multi-State Business Guide"
    meta_description = "Interactive checklist to determine if you need foreign qualification and track your compliance requirements for multi-state business operations."
    
    return render_template('foreign_qualification_checklist.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

# LLC Guides Routes
@app.route('/llc-formation-guide')
def llc_formation_guide():
    """LLC formation guide"""
    title = "LLC Formation Guide - Step-by-Step Business Formation"
    meta_description = "Complete guide to forming an LLC. Learn the step-by-step process, requirements, and best practices for starting your limited liability company."
    
    return render_template('llc_formation_guide.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/llc-operating-agreement-guide')
def llc_operating_agreement_guide():
    """LLC operating agreement guide"""
    title = "LLC Operating Agreement Guide - Essential Business Document"
    meta_description = "Complete guide to LLC operating agreements. Learn what to include, how to create one, and why it's essential for your business."
    
    return render_template('llc_operating_agreement_guide.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/llc-tax-guide')
def llc_tax_guide():
    """LLC tax guide"""
    title = "LLC Tax Guide - Understanding Business Taxation"
    meta_description = "Complete guide to LLC taxation. Learn about pass-through taxation, self-employment taxes, and tax filing requirements for your business."
    
    return render_template('llc_tax_guide.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/llc-compliance-guide')
def llc_compliance_guide():
    """LLC compliance guide"""
    title = "LLC Compliance Guide - Maintaining Your Business Legally"
    meta_description = "Complete guide to LLC compliance requirements. Learn about annual reports, state filings, and maintaining your business in good standing."
    
    return render_template('llc_compliance_guide.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

@app.route('/llc-business-bank-account-guide')
def llc_business_bank_account_guide():
    """LLC business bank account guide"""
    title = "LLC Business Bank Account Guide - Setting Up Business Banking"
    meta_description = "Complete guide to opening a business bank account for your LLC. Learn requirements, documentation, and best practices for business banking."
    
    return render_template('llc_business_bank_account_guide.html',
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_structured_data("WebPage", title, meta_description))

# For Vercel deployment
app.debug = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
