// Check if user is logged in when page loads
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    const username = localStorage.getItem('username');
    if (username) {
        document.getElementById('usernameDisplay').textContent = username;
    }
    
    loadNotes();
    loadTags();
    
    // Setup form submission
    document.getElementById('noteForm').addEventListener('submit', createNote);
});

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        // Redirect to login if no token
        window.location.href = '/login';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

// Get authorization headers
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Create a new note
async function createNote(e) {
    e.preventDefault();
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const tagsInput = document.getElementById('tags').value;
    
    // Convert comma-separated tags to array
    const tag_names = tagsInput
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag !== '');
    
    const noteData = {
        title: title,
        content: content,
        tag_names: tag_names
    };
    
    try {
        const response = await fetch('/notes/', {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(noteData)
        });
        
        if (response.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        if (response.ok) {
            // Clear form
            document.getElementById('noteForm').reset();
            
            // Reload notes
            loadNotes();
            loadTags();
            
            alert('Note created successfully!');
        } else {
            const error = await response.json();
            alert('Error creating note: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating note');
    }
}

// Load all notes
async function loadNotes(tag = null) {
    try {
        let url = '/notes/';
        if (tag) {
            url += `?tag=${encodeURIComponent(tag)}`;
        }
        
        const token = localStorage.getItem('access_token');
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        const notes = await response.json();
        displayNotes(notes);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('notesList').innerHTML = '<p class="empty-state">Error loading notes</p>';
    }
}

// Display notes on the page
function displayNotes(notes) {
    const notesList = document.getElementById('notesList');
    
    if (notes.length === 0) {
        notesList.innerHTML = '<div class="card empty-state"><p>No notes found. Create your first note!</p></div>';
        return;
    }
    
    notesList.innerHTML = notes.map(note => `
        <div class="note-item">
            <div class="note-header">
                <h3 class="note-title">${escapeHtml(note.title)}</h3>
                <div class="note-actions">
                    <button class="btn btn-edit" onclick="editNote(${note.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteNote(${note.id})">Delete</button>
                </div>
            </div>
            <div class="note-content">${escapeHtml(note.content)}</div>
            <div class="note-tags">
                ${note.tags.map(tag => `<span class="tag">${escapeHtml(tag.name)}</span>`).join('')}
            </div>
            <div class="note-date">
                Created: ${new Date(note.created_at).toLocaleString()}
            </div>
        </div>
    `).join('');
}

// Load all available tags for filter dropdown
async function loadTags() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/tags/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.status === 401) {
            return; // Silently fail for tags
        }
        
        const tags = await response.json();
        
        const filterTag = document.getElementById('filterTag');
        
        // Keep "All Notes" option and add tags
        filterTag.innerHTML = '<option value="">All Notes</option>' + 
            tags.map(tag => `<option value="${escapeHtml(tag.name)}">${escapeHtml(tag.name)}</option>`).join('');
    } catch (error) {
        console.error('Error loading tags:', error);
    }
}

// Filter notes by selected tag
function filterNotes() {
    const selectedTag = document.getElementById('filterTag').value;
    if (selectedTag) {
        loadNotes(selectedTag);
    } else {
        loadNotes();
    }
}
// Search notes by keyword
async function searchNotes() {
    const query = document.getElementById('searchQuery').value.trim();
    
    if (!query) {
        alert('Please enter a search keyword');
        return;
    }
    
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/notes/search/?q=${encodeURIComponent(query)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        if (response.ok) {
            const notes = await response.json();
            displayNotes(notes);
            
            if (notes.length === 0) {
                document.getElementById('notesList').innerHTML = 
                    `<div class="card empty-state"><p>No notes found for "${escapeHtml(query)}"</p></div>`;
            }
        } else {
            const error = await response.json();
            alert('Search failed: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error searching notes');
    }
}
// Delete a note
async function deleteNote(noteId) {
    if (!confirm('Are you sure you want to delete this note?')) {
        return;
    }
    
    try {
        const response = await fetch(`/notes/${noteId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (response.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        if (response.ok) {
            loadNotes();
            loadTags();
            alert('Note deleted successfully!');
        } else {
            alert('Error deleting note');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting note');
    }
}

// Edit a note
async function editNote(noteId) {
    try {
        // Get the note details
        const token = localStorage.getItem('access_token');
        const response = await fetch(`/notes/${noteId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        const note = await response.json();
        
        // Prompt for new values
        const newTitle = prompt('Edit Title:', note.title);
        if (newTitle === null) return; // User cancelled
        
        const newContent = prompt('Edit Content:', note.content);
        if (newContent === null) return; // User cancelled
        
        const currentTags = note.tags.map(tag => tag.name).join(', ');
        const newTags = prompt('Edit Tags (comma separated):', currentTags);
        if (newTags === null) return; // User cancelled
        
        // Convert tags to array
        const tag_names = newTags
            .split(',')
            .map(tag => tag.trim())
            .filter(tag => tag !== '');
        
        // Update the note
        const updateResponse = await fetch(`/notes/${noteId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                title: newTitle,
                content: newContent,
                tag_names: tag_names
            })
        });
        
        if (updateResponse.status === 401) {
            alert('Session expired. Please login again.');
            logout();
            return;
        }
        
        if (updateResponse.ok) {
            loadNotes();
            loadTags();
            alert('Note updated successfully!');
        } else {
            alert('Error updating note');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating note');
    }
}

// Helper function to escape HTML and prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}