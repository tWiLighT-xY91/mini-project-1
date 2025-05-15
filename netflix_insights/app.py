from flask import Flask, render_template_string, request #type: ignore
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_analysis import (
    create_engine_connection, get_top_genres, get_shows_per_country,
    get_top_directors, get_yearly_trend, get_type_distribution
)#type: ignore

app = Flask(__name__)
engine = create_engine_connection()

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Netflix Analytics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #111; color: #eee; }
        header { background-color: #e50914; padding: 1rem 2rem; font-size: 1.8rem; font-weight: bold; }
        main { padding: 1rem 2rem; display: flex; flex-direction: column; gap: 2rem;}
        section { background: #222; padding: 1rem; border-radius: 8px; }
        h2 { margin-top: 0; color: #e50914;}
        .chart { height: 400px; }
        footer { text-align: center; margin: 2rem; color: #777; }
        a { color: #e50914; text-decoration: none;}
        a:hover { text-decoration: underline;}
    </style>
</head>
<body>
    <header>Netflix Analytics Dashboard</header>
    <main>
        <section>
            <h2>Top 10 Most Common Genres</h2>
            <div id="genres-chart" class="chart"></div>
        </section>
        <section>
            <h2>Top 10 Countries by Number of Shows</h2>
            <div id="countries-chart" class="chart"></div>
        </section>
        <section>
            <h2>Top 10 Directors</h2>
            <div id="directors-chart" class="chart"></div>
        </section>
        <section>
            <h2>Year-wise Content Trend</h2>
            <div id="years-chart" class="chart"></div>
        </section>
        <section>
            <h2>Content Type Distribution</h2>
            <div id="type-chart" class="chart"></div>
        </section>
    </main>
    <footer>Made with ❤️ by Netflix Insights</footer>

    <script>
        const genresData = {{ genres | safe }};
        const countriesData = {{ countries | safe }};
        const directorsData = {{ directors | safe }};
        const yearsData = {{ years | safe }};
        const typeData = {{ types | safe }};
        
        Plotly.newPlot('genres-chart', {
            data: [{
                x: genresData.listed_in,
                y: genresData.count,
                type: 'bar',
                marker: {color: '#e50914'}
            }],
            layout: {title: '', plot_bgcolor: '#222', paper_bgcolor: '#222', font: {color: '#eee'}}
        });

        Plotly.newPlot('countries-chart', {
            data: [{
                x: countriesData.country,
                y: countriesData.count,
                type: 'bar',
                marker: {color: '#e50914'}
            }],
            layout: {title: '', plot_bgcolor: '#222', paper_bgcolor: '#222', font: {color: '#eee'}}
        });

        Plotly.newPlot('directors-chart', {
            data: [{
                x: directorsData.director,
                y: directorsData.count,
                type: 'bar',
                marker: {color: '#e50914'}
            }],
            layout: {
                title: '',
                plot_bgcolor: '#222',
                paper_bgcolor: '#222',
                font: {color: '#eee'},
                margin: {b: 150},
                xaxis: {tickangle: -45}
            }
        });

        Plotly.newPlot('years-chart', {
            data: [{
                x: yearsData.release_year,
                y: yearsData.count,
                type: 'scatter',
                mode: 'lines+markers',
                line: {color: '#e50914'}
            }],
            layout: {title: '', plot_bgcolor: '#222', paper_bgcolor: '#222', font: {color: '#eee'}}
        });

        Plotly.newPlot('type-chart', {
            data: [{
                labels: typeData.type,
                values: typeData.count,
                type: 'pie',
                marker: {colors: ['#e50914', '#333']}
            }],
            layout: {title: '', plot_bgcolor: '#222', paper_bgcolor: '#222', font: {color: '#eee'}}
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    genres_df = get_top_genres(engine)
    countries_df = get_shows_per_country(engine)
    directors_df = get_top_directors(engine)
    years_df = get_yearly_trend(engine)
    type_df = get_type_distribution(engine)
    
    # Convert dataframes to dict for JSON embedding
    return render_template_string(
        TEMPLATE,
        genres=genres_df.to_dict(orient='list'),
        countries=countries_df.to_dict(orient='list'),
        directors=directors_df.to_dict(orient='list'),
        years=years_df.to_dict(orient='list'),
        types=type_df.to_dict(orient='list')
    )

if __name__ == '__main__':
    app.run(debug=True)
