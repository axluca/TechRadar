# Healthcare Technology Radar

This interactive visualization displays innovative healthcare diagnostic technologies across six key domains, providing insights into their development status, business potential, time to market, and customer desirability.

## Features

- **Interactive Half-Circle Radar Plot**: Visualize technologies in a 180-degree radar format
- **Hover Functionality**: View detailed information about each technology by hovering over bubbles
- **Filtering Options**: Filter technologies by category, TRL, business potential, time to market, and customer desirability
- **Responsive Design**: Works on desktop and mobile devices

## Technology Evaluation Parameters

The visualization uses multiple visual elements to represent different evaluation parameters:

- **Position (Rings)**: Technology Readiness Level (TRL)
  - Inner Ring: Research Phase (TRL 1-3)
  - Middle Ring: Development Phase (TRL 4-6)
  - Outer Ring: Deployment Phase (TRL 7-9)

- **Size**: Business Potential (LOW, MEDIUM, HIGH)
- **Color**: Time to Market (NOW, 1, 3, 5, 10 years)
- **Border Width**: Customer Desirability (LOW, MEDIUM, HIGH)

## Technology Categories

The radar includes technologies from six healthcare domains:

1. Cardiology
2. Neurology
3. Infectious Diseases
4. Continuous Monitoring Systems
5. Oncology
6. Near Patient Care Systems

## Installation and Usage

### Local Development

1. Clone this repository:
```
git clone https://github.com/axluca/Tech-Radar.git
cd Tech-Radar
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the Streamlit app:
```
streamlit run app.py
```

### Deployment

This application is deployed on Streamlit Cloud and can be accessed at: [Healthcare Technology Radar](https://tech-radar.streamlit.app)

## Requirements

- Python 3.7+
- Streamlit
- Plotly
- Pandas
- NumPy

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created by Manus AI
- Based on research of innovative healthcare diagnostic technologies
