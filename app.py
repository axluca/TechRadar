import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Healthcare Technology Radar",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: normal;
        font-style: italic;
        margin-bottom: 2rem;
        text-align: center;
        color: #666;
    }
    .stPlotlyChart {
        height: 800px;
    }
    .hover-info {
        background-color: white;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    /* Make sure the plot maintains aspect ratio */
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">Healthcare Technology Radar</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive visualization of innovative healthcare diagnostic technologies</div>', unsafe_allow_html=True)

# Define the technologies and their attributes
@st.cache_data
def load_technology_data():
    technologies = [
        # Cardiology
        {'name': 'AI-Powered ECG Analysis', 'category': 'Cardiology', 'trl': 8, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Machine learning algorithms that interpret ECG data with greater accuracy and speed than traditional methods, detecting subtle patterns and anomalies.'},
        {'name': 'Wearable Cardiac Monitoring', 'category': 'Cardiology', 'trl': 9, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Advanced wearable monitors providing comprehensive cardiac assessment, including rhythm analysis, heart rate variability, and single-lead ECG capabilities.'},
        {'name': 'Miniaturized Implantable Devices', 'category': 'Cardiology', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Leadless pacemakers and insertable cardiac monitors that are much smaller than traditional implantables, reducing procedural complexity and patient discomfort.'},
        {'name': 'Biomarker-Based Risk Assessment', 'category': 'Cardiology', 'trl': 6, 
         'business': 'MEDIUM', 'time': '3', 'desirability': 'MEDIUM',
         'description': 'Novel biomarker panels that go beyond traditional markers to include genetic markers, inflammatory indicators, and metabolic signatures for personalized risk stratification.'},
        {'name': '3D Bioprinted Cardiac Tissues', 'category': 'Cardiology', 'trl': 4, 
         'business': 'HIGH', 'time': '10', 'desirability': 'HIGH',
         'description': 'Engineered tissues that can serve as personalized testing platforms for drug efficacy and toxicity, enabling more precise treatment selection.'},
        
        # Neurology
        {'name': 'Advanced Neuroimaging', 'category': 'Neurology', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Next-generation technologies including advanced MRI techniques, PET tracers, and hybrid imaging approaches for unprecedented visualization of brain structure and function.'},
        {'name': 'AI Neurological Diagnostics', 'category': 'Neurology', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'HIGH',
         'description': 'AI systems that analyze complex datasets to detect subtle patterns associated with conditions like Parkinson\'s disease, Alzheimer\'s disease, and multiple sclerosis.'},
        {'name': 'Brain-Computer Interfaces', 'category': 'Neurology', 'trl': 5, 
         'business': 'MEDIUM', 'time': '5', 'desirability': 'MEDIUM',
         'description': 'Direct communication pathways between the brain and external devices, enabling both diagnostic assessment and therapeutic intervention.'},
        {'name': 'Neuromodulation Technologies', 'category': 'Neurology', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Advanced systems that combine therapeutic capabilities with diagnostic functions, enabling real-time monitoring of neural activity and treatment response.'},
        {'name': 'Digital Neurological Biomarkers', 'category': 'Neurology', 'trl': 5, 
         'business': 'MEDIUM', 'time': '3', 'desirability': 'MEDIUM',
         'description': 'Objective, quantifiable measures derived from smartphone interactions, wearable sensors, and specialized assessment tools to capture subtle changes in neurological function.'},
        
        # Infectious Diseases
        {'name': 'Rapid Molecular Diagnostics', 'category': 'Infectious Diseases', 'trl': 9, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Advanced platforms enabling rapid, accurate detection of infectious agents through PCR, isothermal amplification, and next-generation sequencing technologies.'},
        {'name': 'AI Pathogen Detection', 'category': 'Infectious Diseases', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'HIGH',
         'description': 'Machine learning algorithms that analyze complex diagnostic data to identify subtle patterns associated with specific infections and predict antimicrobial resistance.'},
        {'name': 'CRISPR Diagnostic Tools', 'category': 'Infectious Diseases', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Technologies utilizing the specific targeting capabilities of CRISPR systems to detect pathogen genetic material with exceptional sensitivity and specificity.'},
        {'name': 'Digital Epidemiology', 'category': 'Infectious Diseases', 'trl': 8, 
         'business': 'MEDIUM', 'time': 'NOW', 'desirability': 'MEDIUM',
         'description': 'Platforms that integrate diverse data sources to track and predict infectious disease spread, enabling earlier detection of outbreaks and more targeted interventions.'},
        {'name': 'Genomic Surveillance', 'category': 'Infectious Diseases', 'trl': 7, 
         'business': 'MEDIUM', 'time': '1', 'desirability': 'MEDIUM',
         'description': 'Systems enabling continuous monitoring of pathogen evolution through regular sequencing and analysis of clinical isolates to detect emerging variants.'},
        
        # Continuous Monitoring
        {'name': 'Advanced CGM', 'category': 'Continuous Monitoring', 'trl': 9, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Continuous glucose monitoring systems providing real-time, dynamic information about glucose levels with improved accuracy, longer sensor life, and predictive alerts.'},
        {'name': 'Multi-Parameter Wearables', 'category': 'Continuous Monitoring', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Advanced wearable systems that simultaneously track multiple physiological parameters for more holistic assessment of health status.'},
        {'name': 'Smart Clothing Sensors', 'category': 'Continuous Monitoring', 'trl': 5, 
         'business': 'MEDIUM', 'time': '3', 'desirability': 'MEDIUM',
         'description': 'Garments with integrated sensors that enable unobtrusive, continuous monitoring during daily activities, tracking parameters like heart activity and respiratory patterns.'},
        {'name': 'Implantable Monitors', 'category': 'Continuous Monitoring', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'MEDIUM',
         'description': 'Devices that provide continuous assessment of specific physiological parameters from within the body, offering exceptional data quality for long-term monitoring.'},
        {'name': 'Remote Patient Monitoring', 'category': 'Continuous Monitoring', 'trl': 8, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Comprehensive platforms that integrate data from various monitoring devices, provide clinical decision support, and facilitate communication between patients and providers.'},
        
        # Oncology
        {'name': 'Liquid Biopsy', 'category': 'Oncology', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Non-invasive cancer detection and monitoring through analysis of circulating tumor DNA, cells, exosomes, and other biomarkers in blood or other bodily fluids.'},
        {'name': 'AI Cancer Diagnostics', 'category': 'Oncology', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'HIGH',
         'description': 'Machine learning systems that analyze complex data to detect subtle patterns associated with malignancy, often with greater sensitivity than human interpretation.'},
        {'name': 'Precision Oncology', 'category': 'Oncology', 'trl': 8, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Diagnostic tools that analyze the genetic and molecular characteristics of tumors to guide personalized treatment decisions and identify actionable mutations.'},
        {'name': 'Digital Pathology', 'category': 'Oncology', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'MEDIUM',
         'description': 'Systems that digitize pathology slides and enable computational analysis to enhance diagnostic accuracy and efficiency, addressing challenges of subjective interpretation.'},
        {'name': 'POC Cancer Diagnostics', 'category': 'Oncology', 'trl': 5, 
         'business': 'MEDIUM', 'time': '3', 'desirability': 'HIGH',
         'description': 'Point-of-care tools enabling rapid, on-site testing for cancer biomarkers, reducing time to diagnosis and expanding access to cancer screening in resource-limited settings.'},
        
        # Near Patient Care
        {'name': 'Portable Molecular Diagnostics', 'category': 'Near Patient Care', 'trl': 8, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Systems performing sophisticated molecular testing outside traditional laboratory settings, detecting specific pathogens and genetic markers with laboratory-grade accuracy.'},
        {'name': 'Microfluidic Lab-on-Chip', 'category': 'Near Patient Care', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'HIGH',
         'description': 'Technologies that integrate multiple laboratory functions on a single chip, performing complex assays with minimal sample volumes and high levels of automation.'},
        {'name': 'Smartphone Diagnostics', 'category': 'Near Patient Care', 'trl': 7, 
         'business': 'HIGH', 'time': '1', 'desirability': 'HIGH',
         'description': 'Systems leveraging the computing power, connectivity, and imaging capabilities of mobile phones to enable sophisticated testing in diverse settings.'},
        {'name': 'Rapid Diagnostic Tests', 'category': 'Near Patient Care', 'trl': 9, 
         'business': 'HIGH', 'time': 'NOW', 'desirability': 'HIGH',
         'description': 'Simple, disposable tests providing visual results without complex instrumentation, typically using lateral flow technologies with results available in minutes.'},
        {'name': 'AI-Enhanced Diagnostics', 'category': 'Near Patient Care', 'trl': 6, 
         'business': 'HIGH', 'time': '3', 'desirability': 'HIGH',
         'description': 'Point-of-care systems incorporating artificial intelligence to improve test interpretation, quality control, and clinical decision support.'},
    ]
    return technologies

# Load the technology data
technologies = load_technology_data()

# Create a DataFrame for easier manipulation
df = pd.DataFrame(technologies)

# Map TRL to radius with clearer grouping
def trl_to_radius(trl):
    if 1 <= trl <= 3:
        return 0.3
    elif 4 <= trl <= 6:
        return 0.6
    else:  # 7-9
        return 0.9

# Apply the mapping to create a new column
df['radius'] = df['trl'].apply(trl_to_radius)

# Map business potential to marker size using log scale for better visibility
business_to_size = {'LOW': 20, 'MEDIUM': 40, 'HIGH': 80}
df['size'] = df['business'].map(business_to_size)

# Map time to market to color with higher contrast
time_to_color = {
    'NOW': '#00441b',  # Dark green
    '1': '#2c7fb8',    # Blue
    '3': '#7fcdbb',    # Teal
    '5': '#fdae61',    # Orange
    '10': '#d7301f',   # Red
    'NEVER': '#7f0000' # Dark red
}
df['color'] = df['time'].map(time_to_color)

# Map customer desirability to marker edge width using log scale for better visibility
# Using logarithmic scale to amplify differences
desirability_to_width = {'LOW': 1, 'MEDIUM': 3, 'HIGH': 9}
df['line_width'] = df['desirability'].map(desirability_to_width)

# Define the categories and their angles (half circle - 180 degrees)
categories = ['Cardiology', 'Neurology', 'Infectious Diseases', 
             'Continuous Monitoring', 'Oncology', 'Near Patient Care']
num_categories = len(categories)

# Create angles for half-circle (0 to pi)
category_angles = np.linspace(0, np.pi, num_categories, endpoint=False)
category_to_angle = {cat: ang for cat, ang in zip(categories, category_angles)}

# Add angle to DataFrame
df['angle'] = df['category'].map(category_to_angle)

# Add some jitter to prevent overlapping
np.random.seed(42)  # For reproducibility
df['angle_jitter'] = df['angle'] + np.random.uniform(-0.15, 0.15, size=len(df))
df['radius_jitter'] = df['radius'] + np.random.uniform(-0.05, 0.05, size=len(df))

# Convert polar coordinates to cartesian for plotting
df['x'] = df['radius_jitter'] * np.cos(df['angle_jitter'])
df['y'] = df['radius_jitter'] * np.sin(df['angle_jitter'])

# Create a container for the hover info
hover_info_container = st.empty()

# Create a session state to store the last hover time and technology
if 'last_hover_time' not in st.session_state:
    st.session_state.last_hover_time = datetime.now() - timedelta(seconds=10)
if 'last_hover_tech' not in st.session_state:
    st.session_state.last_hover_tech = None

# Add sidebar with filters
st.sidebar.title("Filters")

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=categories,
    default=categories
)

# TRL filter
trl_range = st.sidebar.slider(
    "TRL Range",
    min_value=1,
    max_value=9,
    value=(1, 9)
)

# Business Potential filter
business_options = ['LOW', 'MEDIUM', 'HIGH']
selected_business = st.sidebar.multiselect(
    "Business Potential",
    options=business_options,
    default=business_options
)

# Time to Market filter
time_options = ['NOW', '1', '3', '5', '10', 'NEVER']
selected_time = st.sidebar.multiselect(
    "Time to Market",
    options=time_options,
    default=time_options
)

# Customer Desirability filter
desirability_options = ['LOW', 'MEDIUM', 'HIGH']
selected_desirability = st.sidebar.multiselect(
    "Customer Desirability",
    options=desirability_options,
    default=desirability_options
)

# Apply filters to create filtered dataframe
filtered_df = df[
    df['category'].isin(selected_categories) &
    (df['trl'] >= trl_range[0]) & (df['trl'] <= trl_range[1]) &
    df['business'].isin(selected_business) &
    df['time'].isin(selected_time) &
    df['desirability'].isin(selected_desirability)
]

# Create the interactive radar plot with filtered data
def create_radar_plot(filtered_data):
    # Create figure with fixed aspect ratio
    fig = go.Figure()
    
    # Add rings for TRL levels
    ring_radii = [0.3, 0.6, 0.9]
    ring_names = ['Research (TRL 1-3)', 'Development (TRL 4-6)', 'Deployment (TRL 7-9)']
    ring_colors = ['rgba(255,204,204,0.3)', 'rgba(204,238,255,0.3)', 'rgba(204,255,204,0.3)']
    
    for i, radius in enumerate(ring_radii):
        # Create a large number of points to approximate a circle
        theta = np.linspace(0, np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        # Add the ring as a scatter trace with fill
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='gray', width=1, dash='dash'),
            fill='tozeroy' if i == 0 else 'tonexty',
            fillcolor=ring_colors[i],
            name=ring_names[i],
            hoverinfo='skip'
        ))
    
    # Add category lines
    for category, angle in category_to_angle.items():
        x = [0, 1 * np.cos(angle)]
        y = [0, 1 * np.sin(angle)]
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='gray', width=1),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Add category labels
        fig.add_annotation(
            x=1.1 * np.cos(angle),
            y=1.1 * np.sin(angle),
            text=category,
            showarrow=False,
            font=dict(size=14, color='black', family='Arial, sans-serif'),
            bgcolor='white',
            bordercolor='gray',
            borderwidth=1,
            borderpad=4,
            opacity=0.8
        )
    
    # Add technology points from filtered data
    for i, row in filtered_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']],
            mode='markers',
            marker=dict(
                size=row['size'],
                color=row['color'],
                line=dict(width=row['line_width'], color='black'),
                opacity=0.5  # Semi-transparent bubbles for better visibility when overlapping
            ),
            name=row['name'],
            text=row['name'],
            hovertext=f"<b>{row['name']}</b><br>" +
                     f"Category: {row['category']}<br>" +
                     f"TRL: {row['trl']}<br>" +
                     f"Business Potential: {row['business']}<br>" +
                     f"Time to Market: {row['time']}<br>" +
                     f"Customer Desirability: {row['desirability']}",
            hoverinfo='text',
            customdata=[i]  # Store the index for hover callback
        ))
    
    # Update layout with fixed aspect ratio to maintain semicircle shape
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        plot_bgcolor='white',
        title=dict(
            text='Healthcare Technology Radar',
            font=dict(size=24, family='Arial, sans-serif'),
            x=0.5
        ),
        xaxis=dict(
            range=[-1.2, 1.2],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="y",  # This ensures the aspect ratio is maintained
            scaleratio=1      # Equal scaling for x and y axes
        ),
        yaxis=dict(
            range=[0, 1.2],
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        height=700,
        hovermode='closest',
        autosize=True
    )
    
    # Add legends positioned to avoid overlap with the radar plot
    # Time to Market legend - positioned on the right side
    time_items = [
        dict(name='NOW', color='#00441b'),
        dict(name='1 Year', color='#2c7fb8'),
        dict(name='3 Years', color='#7fcdbb'),
        dict(name='5 Years', color='#fdae61'),
        dict(name='10 Years', color='#d7301f')
    ]
    
    # Position legends outside the plot area
    legend_x_right = 1.3
    legend_x_left = -1.3
    
    for i, item in enumerate(time_items):
        fig.add_trace(go.Scatter(
            x=[legend_x_right], y=[0.9 - i*0.1],
            mode='markers',
            marker=dict(size=15, color=item['color'], opacity=0.5),
            name=item['name'],
            showlegend=True,
            hoverinfo='skip'
        ))
    
    # Add annotations for legends
    fig.add_annotation(
        x=legend_x_right, y=1.0,
        text="Time to Market",
        showarrow=False,
        font=dict(size=14, color='black', family='Arial, sans-serif'),
        xanchor='center'
    )
    
    # Business Potential legend - positioned on the left side
    business_items = [
        dict(name='LOW', size=20),
        dict(name='MEDIUM', size=40),
        dict(name='HIGH', size=80)
    ]
    
    for i, item in enumerate(business_items):
        fig.add_trace(go.Scatter(
            x=[legend_x_left], y=[0.9 - i*0.1],
            mode='markers',
            marker=dict(size=item['size']/2, color='gray', opacity=0.5),
            name=item['name'],
            showlegend=True,
            hoverinfo='skip'
        ))
    
    fig.add_annotation(
        x=legend_x_left, y=1.0,
        text="Business Potential",
        showarrow=False,
        font=dict(size=14, color='black', family='Arial, sans-serif'),
        xanchor='center'
    )
    
    # Customer Desirability legend - positioned at the bottom
    desirability_items = [
        dict(name='LOW', width=1),
        dict(name='MEDIUM', width=3),
        dict(name='HIGH', width=9)
    ]
    
    for i, item in enumerate(desirability_items):
        fig.add_trace(go.Scatter(
            x=[-0.4 + i*0.4], y=[0.1],
            mode='markers',
            marker=dict(
                size=30, 
                color='white', 
                opacity=0.5,
                line=dict(width=item['width'], color='black')
            ),
            name=item['name'],
            showlegend=True,
            hoverinfo='skip'
        ))
    
    fig.add_annotation(
        x=0, y=0.2,
        text="Customer Desirability",
        showarrow=False,
        font=dict(size=14, color='black', family='Arial, sans-serif'),
        xanchor='center'
    )
    
    return fig

# Create the plot with filtered data
fig = create_radar_plot(filtered_df)

# Display the plot with config for maintaining aspect ratio
plot_config = {
    'displayModeBar': False,
    'responsive': True,
    'staticPlot': False
}

# Display the plot
st.plotly_chart(fig, use_container_width=True, config=plot_config)

# Check if we should display hover info
current_time = datetime.now()
time_diff = (current_time - st.session_state.last_hover_time).total_seconds()

if st.session_state.last_hover_tech is not None and time_diff < 1.5:
    tech = st.session_state.last_hover_tech
    with hover_info_container:
        st.markdown(f"""
        <div class="hover-info">
            <h3>{tech['name']}</h3>
            <p><strong>Category:</strong> {tech['category']}</p>
            <p><strong>TRL:</strong> {tech['trl']} ({['Research', 'Development', 'Deployment'][int(tech['radius']/0.3) - 1]} Phase)</p>
            <p><strong>Business Potential:</strong> {tech['business']}</p>
            <p><strong>Time to Market:</strong> {tech['time']}</p>
            <p><strong>Customer Desirability:</strong> {tech['desirability']}</p>
            <p><strong>Description:</strong> {tech['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# Display filtered technologies in a table
st.sidebar.title("Filtered Technologies")
if not filtered_df.empty:
    for _, tech in filtered_df.iterrows():
        st.sidebar.markdown(f"""
        <div style="margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
            <strong>{tech['name']}</strong><br>
            Category: {tech['category']}<br>
            TRL: {tech['trl']}<br>
            Business: {tech['business']}<br>
            Time: {tech['time']}<br>
            Desirability: {tech['desirability']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.sidebar.write("No technologies match the selected filters.")

# Add information about the project
st.sidebar.markdown("---")
st.sidebar.title("About")
st.sidebar.info(
    """
    This interactive Technology Radar visualizes innovative healthcare diagnostic technologies 
    across six key domains. Hover over the bubbles to see detailed information about each technology.
    
    The visualization uses:
    - **Position**: Technology Readiness Level (TRL)
    - **Size**: Business Potential
    - **Color**: Time to Market
    - **Border Width**: Customer Desirability (log scale)
    
    Created by Manus AI
    """
)
