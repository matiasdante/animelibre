from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os

# Add the parent directory to the path to import existing modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

try:
    from scripts.anime_scrapper import AnimeFLV
    from api.anime_api import AnimeAPI
    from api.vlc_handler import VLCHandler
except ImportError:
    # If running from within web directory, try different path
    grandparent_dir = os.path.dirname(parent_dir)
    sys.path.append(grandparent_dir)
    from scripts.anime_scrapper import AnimeFLV
    from api.anime_api import AnimeAPI
    from api.vlc_handler import VLCHandler
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'anime_libre_secret_key_2024'

# Initialize components
anime_api = AnimeAPI()
vlc_handler = VLCHandler()

# Database initialization
def init_db():
    """Initialize SQLite database for history and configuration"""
    conn = sqlite3.connect('anime_libre.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_title TEXT,
            anime_id TEXT,
            episode_number INTEGER,
            watch_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cover_url TEXT
        )
    ''')
    
    # Set default player if not exists
    cursor.execute('INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)', 
                   ('player', 'vlc'))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Main page with changelog and recent animes"""
    # Get recent animes from history
    conn = sqlite3.connect('anime_libre.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT anime_title, anime_id, cover_url, MAX(watch_date) as last_watched
        FROM history 
        GROUP BY anime_id
        ORDER BY last_watched DESC 
        LIMIT 6
    ''')
    recent_animes = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', recent_animes=recent_animes)

@app.route('/search')
def search():
    """Search page for animes"""
    return render_template('search.html')

@app.route('/anime/<anime_id>')
def anime_detail(anime_id):
    """Anime detail page with episodes"""
    anime_info = anime_api.get_anime_info(anime_id)
    if not anime_info:
        return "Anime not found", 404
    
    return render_template('anime_detail.html', anime=anime_info, anime_id=anime_id)

@app.route('/api/search')
def api_search():
    """API endpoint for anime search"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        results = anime_api.search_anime(query)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anime/<anime_id>')
def api_anime_info(anime_id):
    """API endpoint for anime information"""
    try:
        anime_info = anime_api.get_anime_info(anime_id)
        if not anime_info:
            return jsonify({'error': 'Anime not found'}), 404
        return jsonify(anime_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anime/<anime_id>/episodes')
def api_anime_episodes(anime_id):
    """API endpoint for anime episodes"""
    try:
        episodes = anime_api.get_anime_episodes(anime_id)
        return jsonify({'episodes': episodes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/episode/links')
def api_episode_links():
    """API endpoint for episode video links"""
    anime_id = request.args.get('anime_id')
    episode_num = request.args.get('episode')
    
    if not anime_id or not episode_num:
        return jsonify({'error': 'anime_id and episode parameters required'}), 400
    
    try:
        links = anime_api.get_episode_links(anime_id, int(episode_num))
        return jsonify({'links': links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/play', methods=['POST'])
def api_play_video():
    """API endpoint to play video with configured player"""
    data = request.get_json()
    video_url = data.get('url')
    anime_title = data.get('anime_title', '')
    episode_num = data.get('episode', 1)
    
    if not video_url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        # Get configured player
        conn = sqlite3.connect('anime_libre.db')
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM config WHERE key = ?', ('player',))
        result = cursor.fetchone()
        player = result[0] if result else 'vlc'
        conn.close()
        
        # Play video
        success = vlc_handler.play_video(video_url, player, f"{anime_title} - Episode {episode_num}")
        
        if success:
            return jsonify({'status': 'success', 'message': 'Video opened in player'})
        else:
            return jsonify({'error': 'Failed to open video'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['POST'])
def api_add_history():
    """API endpoint to add anime to history"""
    data = request.get_json()
    anime_title = data.get('anime_title')
    anime_id = data.get('anime_id')
    episode_num = data.get('episode')
    cover_url = data.get('cover_url', '')
    
    if not all([anime_title, anime_id, episode_num]):
        return jsonify({'error': 'anime_title, anime_id, and episode required'}), 400
    
    try:
        conn = sqlite3.connect('anime_libre.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO history (anime_title, anime_id, episode_number, cover_url)
            VALUES (?, ?, ?, ?)
        ''', (anime_title, anime_id, episode_num, cover_url))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """History page showing watched animes"""
    conn = sqlite3.connect('anime_libre.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT anime_title, anime_id, GROUP_CONCAT(episode_number) as episodes, 
               cover_url, MAX(watch_date) as last_watched
        FROM history 
        GROUP BY anime_id
        ORDER BY last_watched DESC
    ''')
    history_data = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', history=history_data)

@app.route('/settings')
def settings():
    """Settings page for player configuration"""
    conn = sqlite3.connect('anime_libre.db')
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM config WHERE key = ?', ('player',))
    result = cursor.fetchone()
    current_player = result[0] if result else 'vlc'
    conn.close()
    
    return render_template('settings.html', current_player=current_player)

@app.route('/api/settings', methods=['POST'])
def api_save_settings():
    """API endpoint to save settings"""
    data = request.get_json()
    player = data.get('player')
    
    if player not in ['vlc', 'mpv', 'default']:
        return jsonify({'error': 'Invalid player option'}), 400
    
    try:
        conn = sqlite3.connect('anime_libre.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', 
                       ('player', player))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/remove', methods=['POST'])
def api_remove_history():
    """API endpoint to remove anime from history"""
    data = request.get_json()
    anime_id = data.get('anime_id')
    
    if not anime_id:
        return jsonify({'error': 'anime_id required'}), 400
    
    try:
        conn = sqlite3.connect('anime_libre.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history WHERE anime_id = ?', (anime_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/player/check')
def api_check_player():
    """API endpoint to check player availability"""
    player = request.args.get('player', 'vlc')
    
    try:
        available = vlc_handler.is_player_available(player)
        return jsonify({'available': available})
    except Exception as e:
        return jsonify({'available': False, 'error': str(e)})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)