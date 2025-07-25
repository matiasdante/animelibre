import sys
import os

# Add the parent directory to the path to import existing modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

try:
    from scripts.anime_scrapper import AnimeFLV
except ImportError:
    # If running from within web directory, try different path
    grandparent_dir = os.path.dirname(parent_dir)
    sys.path.append(grandparent_dir)
    from scripts.anime_scrapper import AnimeFLV

class AnimeAPI:
    """API wrapper for anime functionality"""
    
    def __init__(self):
        self.api = AnimeFLV()
        self.current_anime_info = None
    
    def search_anime(self, query):
        """Search for animes and return formatted results"""
        try:
            results = self.api.search(query)
            formatted_results = []
            
            for anime_id in results:
                # Convert anime_id to display title by replacing hyphens with spaces and capitalizing
                display_title = anime_id.replace('-', ' ').title()
                formatted_results.append({
                    'id': anime_id,
                    'title': display_title
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error searching anime: {e}")
            return []
    
    def get_anime_info(self, anime_id):
        """Get detailed information about an anime"""
        try:
            self.api.anime_info(anime_id)
            
            anime_info = {
                'id': anime_id,
                'title': self.api.anime_title(),
                'status': self.api.anime_status(),
                'summary': self.api.anime_summary(),
                'cover': self.api.anime_cover(),
                'episodes': self.api.anime_episodes()
            }
            
            self.current_anime_info = anime_info
            return anime_info
            
        except Exception as e:
            print(f"Error getting anime info: {e}")
            return None
    
    def get_anime_episodes(self, anime_id):
        """Get list of episodes for an anime"""
        try:
            if not self.current_anime_info or self.current_anime_info['id'] != anime_id:
                self.get_anime_info(anime_id)
            
            if self.current_anime_info:
                episodes = self.current_anime_info['episodes']
                formatted_episodes = []
                
                for i, episode in enumerate(episodes, 1):
                    formatted_episodes.append({
                        'number': i,
                        'id': episode,
                        'title': f"Episodio {i}"
                    })
                
                return formatted_episodes
            
            return []
            
        except Exception as e:
            print(f"Error getting episodes: {e}")
            return []
    
    def get_episode_links(self, anime_id, episode_number):
        """Get video links for a specific episode"""
        try:
            if not self.current_anime_info or self.current_anime_info['id'] != anime_id:
                self.get_anime_info(anime_id)
            
            if self.current_anime_info:
                links = self.api.get_links(episode_number)
                formatted_links = []
                
                for link in links:
                    # Determine provider based on URL
                    provider = "Unknown"
                    if "ok.ru" in link:
                        provider = "OK.ru"
                    elif "yourupload.com" in link:
                        provider = "YourUpload"
                    elif "streamwish.to" in link:
                        provider = "StreamWish"
                    
                    formatted_links.append({
                        'url': link,
                        'provider': provider
                    })
                
                return formatted_links
            
            return []
            
        except Exception as e:
            print(f"Error getting episode links: {e}")
            return []