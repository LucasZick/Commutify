import os
import osmnx as ox
import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

# Caminho para a pasta 'maps'
MAPS_FOLDER = os.path.join(os.getcwd(), 'maps')

def create_maps_folder():
    if not os.path.exists(MAPS_FOLDER):
        os.makedirs(MAPS_FOLDER)

def check_existing_map(city_name):
    file_name = f'{city_name.lower().replace(" ", "_")}.html'
    if os.path.exists(os.path.join(MAPS_FOLDER, file_name)):
        # Verificar a data de modificação
        mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(MAPS_FOLDER, file_name)))
        current_time = datetime.now()
        if (current_time - mod_time) < timedelta(days=30):
            return file_name  # Retornar o arquivo existente se for recente o suficiente

    return None

def generate_folium_map(place_name):
    try:
        # Obter o contorno da cidade
        city = ox.geocode_to_gdf(place_name)
        city_boundary = city.geometry.iloc[0]

        # Baixar os dados do OpenStreetMap para pontos de ônibus dentro do contorno da cidade
        tags = {"highway": "bus_stop"}
        bus_stops_osmnx = ox.geometries_from_polygon(city_boundary, tags)

        # Filtrar para obter apenas os pontos de ônibus (geometry type == Point)
        bus_stops_osmnx = bus_stops_osmnx[bus_stops_osmnx["geometry"].apply(lambda x: x.geom_type == "Point")]

        # Calcular o zoom inicial com base na largura da cidade
        bounds = city_boundary.bounds
        if bounds:
            # Calcular o zoom inicial de acordo com a largura da cidade
            zoom = 12 - int(max(bounds[2] - bounds[0], bounds[3] - bounds[1]) * 0.1)  # Ajuste do zoom
        else:
            zoom = 12  # Valor padrão de zoom

        # Criar mapa da cidade
        mapa = folium.Map(location=[city_boundary.centroid.y, city_boundary.centroid.x], zoom_start=zoom)

        # Adicionar círculos azuis nos pontos de ônibus
        for idx, row in bus_stops_osmnx.iterrows():
            coords = (row.geometry.y, row.geometry.x)  # Coordenadas do ponto de ônibus
            folium.Circle(location=coords, radius=5, color='blue', fill=True, fill_color='blue').add_to(mapa)

        # Adicionar o contorno da cidade
        folium.GeoJson(city_boundary.__geo_interface__, style_function=lambda x: {'color': 'red', 'weight': 1}).add_to(mapa)

        # Preparar dados para o mapa de calor
        heat_data = [[point.geometry.y, point.geometry.x] for idx, point in bus_stops_osmnx.iterrows()]

        # Criar o mapa de calor
        HeatMap(heat_data, radius=25, max_zoom=15).add_to(mapa)

        # Salvar o mapa como HTML na pasta maps
        create_maps_folder()
        file_name = f'{place_name.lower().replace(" ", "_")}.html'
        mapa.save(os.path.join(MAPS_FOLDER, file_name))
        print(f'Mapa de calor salvo em: {os.path.join(MAPS_FOLDER, file_name)}')

        return file_name

    except Exception as e:
        print(f"Erro ao processar a cidade '{place_name}': {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        place_name = request.form['city']
        try:
            # Verificar se já existe um mapa para esta cidade e se é recente
            existing_map = check_existing_map(place_name)
            if existing_map:
                return redirect(url_for('index', city=place_name, map_file=existing_map))

            # Gerar o mapa do folium
            map_file = generate_folium_map(place_name)

            if map_file:
                return redirect(url_for('index', city=place_name, map_file=map_file))
            else:
                error_message = f"Erro ao processar a cidade '{place_name}'. Tente novamente mais tarde."
                return render_template('index.html', error=error_message)

        except Exception as e:
            error_message = f"Erro ao processar a cidade '{place_name}': {str(e)}"
            return render_template('index.html', error=error_message)

    city = request.args.get('city', '')
    map_file = request.args.get('map_file', '')
    return render_template('index.html', city=city, map_file=map_file)

@app.route('/maps/<filename>')
def show_map(filename):
    return send_from_directory(MAPS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
