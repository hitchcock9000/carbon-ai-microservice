"""
FastAPI endpoint for AI-powered emissions insights.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import statistics
import os
from openai import OpenAI

router = APIRouter()

# Initialize OpenAI client
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        print("✓ OpenAI client initialized for insights")
    else:
        print("⚠️  OPENAI_API_KEY not found. AI insights will use rule-based analysis only.")
except Exception as e:
    print(f"⚠️  Failed to initialize OpenAI: {e}")


class EmissionRecord(BaseModel):
    """Single emission record."""
    date: str = Field(..., description="Date in ISO format")
    category: str = Field(..., description="Emission category")
    amount: float = Field(..., description="CO2e amount in kg")
    description: Optional[str] = None


class InsightsRequest(BaseModel):
    """Request for emissions insights."""
    emissions: List[EmissionRecord] = Field(..., description="List of emission records")
    use_ai: bool = Field(default=True, description="Use AI-powered insights")


class CategoryStat(BaseModel):
    """Category statistics."""
    category: str
    total: float
    percentage: float
    count: int


class MonthlyTrend(BaseModel):
    """Monthly trend data."""
    month: str
    total: float
    count: int
    average: float
    change: Optional[float] = None
    change_absolute: Optional[float] = None


class Spike(BaseModel):
    """Spike detection result."""
    month: Optional[str] = None
    total: Optional[float] = None
    change: Optional[float] = None


class Recommendation(BaseModel):
    """AI-powered recommendation."""
    type: str
    priority: str
    title: str
    description: str
    impact: str
    effort: str
    icon: str


class InsightsResponse(BaseModel):
    """Response with emissions insights."""
    total_emissions: float
    category_ranking: List[CategoryStat]
    monthly_trends: List[MonthlyTrend]
    biggest_spike: Optional[Spike]
    biggest_drop: Optional[Spike]
    volatility: float
    recommendations: List[Recommendation]
    ai_summary: Optional[str] = None


def get_category_ranking(emissions: List[EmissionRecord]) -> List[CategoryStat]:
    """Calculate category ranking by total emissions."""
    category_totals = {}
    category_counts = {}
    
    for emission in emissions:
        cat = emission.category
        amount = emission.amount
        
        category_totals[cat] = category_totals.get(cat, 0) + amount
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    total_emissions = sum(category_totals.values())
    
    ranking = [
        CategoryStat(
            category=cat,
            total=total,
            percentage=(total / total_emissions * 100) if total_emissions > 0 else 0,
            count=category_counts[cat]
        )
        for cat, total in category_totals.items()
    ]
    
    ranking.sort(key=lambda x: x.total, reverse=True)
    return ranking


def get_monthly_trends(emissions: List[EmissionRecord]) -> List[MonthlyTrend]:
    """Analyze monthly trends."""
    monthly_data = {}
    
    for emission in emissions:
        try:
            date = datetime.fromisoformat(emission.date.replace('Z', '+00:00'))
            month_key = date.strftime('%Y-%m')
            
            if month_key not in monthly_data:
                monthly_data[month_key] = {'total': 0, 'count': 0}
            
            monthly_data[month_key]['total'] += emission.amount
            monthly_data[month_key]['count'] += 1
        except Exception as e:
            print(f"Warning: Failed to parse date {emission.date}: {e}")
            continue
    
    # Convert to sorted list
    trends = [
        MonthlyTrend(
            month=month,
            total=data['total'],
            count=data['count'],
            average=data['total'] / data['count']
        )
        for month, data in sorted(monthly_data.items())
    ]
    
    # Calculate month-over-month changes
    for i in range(1, len(trends)):
        current = trends[i].total
        previous = trends[i - 1].total
        
        if previous != 0:
            trends[i].change = ((current - previous) / previous) * 100
        else:
            trends[i].change = 0
        
        trends[i].change_absolute = current - previous
    
    return trends


def detect_spikes(trends: List[MonthlyTrend]) -> tuple:
    """Detect biggest spikes and volatility."""
    if len(trends) < 2:
        return None, None, 0.0
    
    trends_with_change = [t for t in trends if t.change is not None]
    
    if not trends_with_change:
        return None, None, 0.0
    
    biggest_increase = max(trends_with_change, key=lambda t: t.change or 0)
    biggest_decrease = min(trends_with_change, key=lambda t: t.change or 0)
    
    # Calculate volatility (standard deviation of changes)
    changes = [t.change for t in trends_with_change if t.change is not None]
    volatility = statistics.stdev(changes) if len(changes) > 1 else 0.0
    
    spike_increase = Spike(
        month=biggest_increase.month,
        total=biggest_increase.total,
        change=biggest_increase.change
    ) if biggest_increase.change and biggest_increase.change > 0 else None
    
    spike_decrease = Spike(
        month=biggest_decrease.month,
        total=biggest_decrease.total,
        change=biggest_decrease.change
    ) if biggest_decrease.change and biggest_decrease.change < 0 else None
    
    return spike_increase, spike_decrease, volatility


def generate_rule_based_recommendations(
    category_ranking: List[CategoryStat],
    spike: Optional[Spike],
    total_emissions: float
) -> List[Recommendation]:
    """Generate recommendations based on rules."""
    recommendations = []
    
    if not category_ranking:
        return recommendations
    
    top_category = category_ranking[0]
    cat_name = top_category.category.lower()
    
    # Category-based recommendations
    if 'energy' in cat_name or 'eletricidade' in cat_name or 'energia' in cat_name:
        recommendations.append(Recommendation(
            type='energy',
            priority='high',
            title='Optimize Energy Consumption',
            description=f'Energy is your largest emission source ({top_category.percentage:.1f}%). Consider LED lighting, HVAC optimization, and energy audits.',
            impact='high',
            effort='medium',
            icon='⚡'
        ))
    elif 'transport' in cat_name or 'transporte' in cat_name:
        recommendations.append(Recommendation(
            type='transport',
            priority='high',
            title='Reduce Transportation Emissions',
            description=f'Transportation accounts for {top_category.percentage:.1f}% of emissions. Promote remote work, public transit, or electric vehicles.',
            impact='high',
            effort='medium',
            icon='🚗'
        ))
    elif 'waste' in cat_name or 'resíduos' in cat_name:
        recommendations.append(Recommendation(
            type='waste',
            priority='medium',
            title='Improve Waste Management',
            description='Implement recycling programs, reduce single-use plastics, and explore composting.',
            impact='medium',
            effort='low',
            icon='♻️'
        ))
    else:
        recommendations.append(Recommendation(
            type='general',
            priority='medium',
            title=f'Reduce {top_category.category} Emissions',
            description=f'{top_category.category} represents {top_category.percentage:.1f}% of emissions. Identify key drivers and optimization opportunities.',
            impact='medium',
            effort='medium',
            icon='🎯'
        ))
    
    # Spike-based recommendations
    if spike and spike.change and spike.change > 20:
        recommendations.append(Recommendation(
            type='trend',
            priority='high',
            title='Investigate Emission Spike',
            description=f'Emissions increased by {spike.change:.1f}% in {spike.month}. Identify root causes and implement corrective actions.',
            impact='high',
            effort='low',
            icon='📈'
        ))
    
    # Quick wins
    recommendations.append(Recommendation(
        type='quick-win',
        priority='low',
        title='Quick Win: Employee Awareness',
        description='Launch carbon footprint awareness campaign for employees to drive behavioral change.',
        impact='low',
        effort='low',
        icon='💡'
    ))
    
    # Reduction target
    potential_reduction = top_category.total * 0.15
    recommendations.append(Recommendation(
        type='target',
        priority='medium',
        title=f'Target: Reduce {potential_reduction:.0f} kg CO₂e',
        description=f'By optimizing {top_category.category}, you can potentially save 15% of emissions.',
        impact='high',
        effort='medium',
        icon='🎯'
    ))
    
    return recommendations


def generate_ai_summary(
    emissions: List[EmissionRecord],
    category_ranking: List[CategoryStat],
    trends: List[MonthlyTrend],
    total_emissions: float
) -> Optional[str]:
    """Generate AI-powered summary using OpenAI."""
    if not client:
        return None
    
    try:
        # Prepare context
        categories_text = ", ".join([
            f"{cat.category} ({cat.percentage:.1f}%)"
            for cat in category_ranking[:3]
        ])
        
        trend_text = ""
        if len(trends) >= 2:
            recent = trends[-1]
            if recent.change:
                trend_text = f"Recent trend: {recent.change:+.1f}% change in {recent.month}"
        
        prompt = f"""Analyze this company's carbon emissions data:

Total Emissions: {total_emissions:.0f} kg CO₂e
Number of Records: {len(emissions)}
Top Categories: {categories_text}
{trend_text}

Provide a 2-3 sentence executive summary highlighting:
1. The most critical emission source
2. Key trend or pattern
3. One actionable recommendation

Be concise, professional, and focused on ESG best practices."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an ESG analyst specialized in carbon emissions. Provide concise, actionable insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"⚠️  AI summary generation failed: {e}")
        return None


@router.post("/analyze", response_model=InsightsResponse)
async def analyze_emissions(request: InsightsRequest):
    """
    Analyze emissions data and provide AI-powered insights.
    
    **Features:**
    - Category ranking and breakdown
    - Monthly trend analysis
    - Spike detection
    - Rule-based recommendations
    - Optional AI-powered summary (requires OpenAI API key)
    
    **Example Request:**
    ```json
    {
      "emissions": [
        {
          "date": "2024-01-15",
          "category": "Electricity",
          "amount": 1500.5,
          "description": "Office building"
        }
      ],
      "use_ai": true
    }
    ```
    """
    try:
        if not request.emissions:
            raise HTTPException(
                status_code=400,
                detail="No emissions data provided"
            )
        
        # Calculate total emissions
        total_emissions = sum(e.amount for e in request.emissions)
        
        # Category analysis
        category_ranking = get_category_ranking(request.emissions)
        
        # Monthly trends
        monthly_trends = get_monthly_trends(request.emissions)
        
        # Spike detection
        spike_increase, spike_decrease, volatility = detect_spikes(monthly_trends)
        
        # Generate recommendations
        recommendations = generate_rule_based_recommendations(
            category_ranking,
            spike_increase,
            total_emissions
        )
        
        # AI summary (if enabled and available)
        ai_summary = None
        if request.use_ai and client:
            ai_summary = generate_ai_summary(
                request.emissions,
                category_ranking,
                monthly_trends,
                total_emissions
            )
        
        return InsightsResponse(
            total_emissions=total_emissions,
            category_ranking=category_ranking,
            monthly_trends=monthly_trends,
            biggest_spike=spike_increase,
            biggest_drop=spike_decrease,
            volatility=volatility,
            recommendations=recommendations,
            ai_summary=ai_summary
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze emissions: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Check insights service health."""
    return {
        "status": "healthy",
        "openai_available": client is not None,
        "features": {
            "category_analysis": True,
            "trend_analysis": True,
            "spike_detection": True,
            "rule_based_recommendations": True,
            "ai_summary": client is not None
        }
    }
