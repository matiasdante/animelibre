// Global JavaScript for Anime Libre

// Utility functions
const AnimeLibre = {
    // Show loading modal
    showLoading: function(message = 'Cargando...') {
        const modal = document.getElementById('loadingModal');
        const modalBody = modal.querySelector('.modal-body p');
        if (modalBody) {
            modalBody.textContent = message;
        }
        const bootstrap_modal = new bootstrap.Modal(modal);
        bootstrap_modal.show();
        return bootstrap_modal;
    },

    // Hide loading modal
    hideLoading: function() {
        const modal = document.getElementById('loadingModal');
        const bootstrap_modal = bootstrap.Modal.getInstance(modal);
        if (bootstrap_modal) {
            bootstrap_modal.hide();
        }
    },

    // Show error toast
    showError: function(message) {
        const toast = document.getElementById('errorToast');
        const toastBody = document.getElementById('errorToastBody');
        toastBody.textContent = message;
        const bootstrap_toast = new bootstrap.Toast(toast);
        bootstrap_toast.show();
    },

    // Show success toast
    showSuccess: function(message) {
        const toast = document.getElementById('successToast');
        const toastBody = document.getElementById('successToastBody');
        toastBody.textContent = message;
        const bootstrap_toast = new bootstrap.Toast(toast);
        bootstrap_toast.show();
    },

    // API calls
    api: {
        // Search animes
        searchAnimes: async function(query) {
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error en la búsqueda');
                }
                
                return data.results;
            } catch (error) {
                console.error('Error searching animes:', error);
                throw error;
            }
        },

        // Get anime info
        getAnimeInfo: async function(animeId) {
            try {
                const response = await fetch(`/api/anime/${animeId}`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error obteniendo información del anime');
                }
                
                return data;
            } catch (error) {
                console.error('Error getting anime info:', error);
                throw error;
            }
        },

        // Get anime episodes
        getAnimeEpisodes: async function(animeId) {
            try {
                const response = await fetch(`/api/anime/${animeId}/episodes`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error obteniendo episodios');
                }
                
                return data.episodes;
            } catch (error) {
                console.error('Error getting episodes:', error);
                throw error;
            }
        },

        // Get episode links
        getEpisodeLinks: async function(animeId, episode) {
            try {
                const response = await fetch(`/api/episode/links?anime_id=${animeId}&episode=${episode}`);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error obteniendo enlaces');
                }
                
                return data.links;
            } catch (error) {
                console.error('Error getting episode links:', error);
                throw error;
            }
        },

        // Play video
        playVideo: async function(url, animeTitle = '', episode = 1) {
            try {
                const response = await fetch('/api/play', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: url,
                        anime_title: animeTitle,
                        episode: episode
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error reproduciendo video');
                }
                
                return data;
            } catch (error) {
                console.error('Error playing video:', error);
                throw error;
            }
        },

        // Add to history
        addToHistory: async function(animeTitle, animeId, episode, coverUrl = '') {
            try {
                const response = await fetch('/api/history', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        anime_title: animeTitle,
                        anime_id: animeId,
                        episode: episode,
                        cover_url: coverUrl
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error agregando al historial');
                }
                
                return data;
            } catch (error) {
                console.error('Error adding to history:', error);
                throw error;
            }
        },

        // Save settings
        saveSettings: async function(settings) {
            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(settings)
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Error guardando configuración');
                }
                
                return data;
            } catch (error) {
                console.error('Error saving settings:', error);
                throw error;
            }
        }
    },

    // Utility functions
    utils: {
        // Debounce function for search
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Format anime title for display
        formatAnimeTitle: function(title) {
            return title.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        },

        // Get provider icon
        getProviderIcon: function(provider) {
            const icons = {
                'OK.ru': 'fas fa-play-circle',
                'YourUpload': 'fas fa-upload',
                'StreamWish': 'fas fa-stream',
                'Unknown': 'fas fa-video'
            };
            return icons[provider] || icons['Unknown'];
        },

        // Get provider color
        getProviderColor: function(provider) {
            const colors = {
                'OK.ru': 'primary',
                'YourUpload': 'success',
                'StreamWish': 'info',
                'Unknown': 'secondary'
            };
            return colors[provider] || colors['Unknown'];
        },

        // Add fade in animation to elements
        addFadeInAnimation: function(elements) {
            if (typeof elements === 'string') {
                elements = document.querySelectorAll(elements);
            } else if (elements.nodeType) {
                elements = [elements];
            }

            elements.forEach((element, index) => {
                setTimeout(() => {
                    element.classList.add('fade-in');
                }, index * 100);
            });
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add fade in animation to cards
    AnimeLibre.utils.addFadeInAnimation('.card');
    
    // Handle navigation active state
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Export for use in other scripts
window.AnimeLibre = AnimeLibre;