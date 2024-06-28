from flask import Flask, jsonify, request, render_template
import pandas as pd
import datetime

app = Flask(__name__)

resources_df = pd.read_csv('data/resources.csv')
resources_df['last_updated'] = datetime.datetime.now()
resources_df = resources_df.where(pd.notnull(resources_df), None)

# API to get resource data
@app.route('/api/resources', methods=['GET'])
def get_resources():
    data = resources_df.to_dict(orient='records')
    return jsonify(data)

# API to update resource status
@app.route('/api/update_status', methods=['POST'])
def update_status():
    resource_id = request.json['resource_id']
    new_status = request.json['new_status']
    resources_df.loc[resources_df['place_id'] == resource_id, 'business_status'] = new_status
    resources_df.loc[resources_df['place_id'] == resource_id, 'last_updated'] = datetime.datetime.now()
    return jsonify({'status': 'success'})

# API to update resource location
@app.route('/api/update_location', methods=['POST'])
def update_location():
    resource_id = request.json['resource_id']
    new_location = request.json['new_location']
    resources_df.loc[resources_df['place_id'] == resource_id, ['geometry/location/lat', 'geometry/location/lng']] = new_location
    resources_df.loc[resources_df['place_id'] == resource_id, 'last_updated'] = datetime.datetime.now()
    return jsonify({'status': 'success'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
