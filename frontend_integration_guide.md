# 🎨 Frontend Integration Guide - Real Knowledge Base

## 📋 Overview

Questo documento spiega come integrare il sistema di Knowledge Base reale nel frontend, sostituendo i dati mock con documenti reali dalla knowledge base di Siebert.

## 🔄 Cambiamenti Necessari nel Frontend

### **1. Endpoint per Documenti Reali**

**Sostituire l'endpoint mock con:**
```javascript
// Invece di dati mock hardcoded
const mockDocuments = [
  {
    id: "financial-trends-2024",
    title: "Financial Market Trends 2024",
    description: "Comprehensive analysis of current market trends...",
    date: "Jan 15, 2024",
    category: "market_analysis",
    tags: ["finance", "markets", "2024"],
    selected: false
  },
  // ...
];

// Usare chiamata API reale
const fetchRealDocuments = async (clientName = 'siebert') => {
  try {
    const response = await fetch(
      `http://localhost:8001/api/v1/knowledge-base/frontend/clients/${clientName}/documents`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const documents = await response.json();
    return documents;
  } catch (error) {
    console.error('Error fetching documents:', error);
    return [];
  }
};
```

### **2. Formato Dati Compatibile**

I documenti reali hanno questo formato (già compatibile con il frontend):

```json
[
  {
    "id": "content_guidelines",
    "title": "Siebert Financial - Content Creation Guidelines",
    "description": "Our content strategy focuses on empowering Gen Z and Millennial investors...",
    "date": "2025-07-25",
    "category": "style",
    "tags": ["style", "gen-z", "markets", "content", "guidelines", "finance", "investing"],
    "selected": false
  },
  {
    "id": "company_profile", 
    "title": "Siebert Financial Corp - Company Profile",
    "description": "Siebert Financial Corp is a pioneering financial services company...",
    "date": "2025-07-25",
    "category": "gen-z",
    "tags": ["gen-z", "profile", "markets", "finance", "company", "investing"],
    "selected": false
  }
]
```

### **3. Implementazione React/Vue**

**React Example:**
```jsx
import React, { useState, useEffect } from 'react';

const KnowledgeBaseSelector = ({ clientName = 'siebert', onDocumentsChange }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);

  // Fetch documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, [clientName]);

  const fetchDocuments = async (search = '', tags = []) => {
    setLoading(true);
    setError(null);
    
    try {
      let url = `http://localhost:8001/api/v1/knowledge-base/frontend/clients/${clientName}/documents`;
      
      // Add query parameters
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      tags.forEach(tag => params.append('tags', tag));
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const docs = await response.json();
      setDocuments(docs);
      
      // Notify parent component
      if (onDocumentsChange) {
        onDocumentsChange(docs);
      }
      
    } catch (err) {
      setError(err.message);
      console.error('Error fetching documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentToggle = (docId) => {
    const updatedDocs = documents.map(doc => 
      doc.id === docId 
        ? { ...doc, selected: !doc.selected }
        : doc
    );
    setDocuments(updatedDocs);
    
    if (onDocumentsChange) {
      onDocumentsChange(updatedDocs);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    fetchDocuments(query, selectedTags);
  };

  const handleTagFilter = (tags) => {
    setSelectedTags(tags);
    fetchDocuments(searchQuery, tags);
  };

  if (loading) return <div>Loading documents...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="knowledge-base-selector">
      <h3>Knowledge Base Content ({documents.length} available)</h3>
      
      {/* Search */}
      <input
        type="text"
        placeholder="Search content..."
        value={searchQuery}
        onChange={(e) => handleSearch(e.target.value)}
      />
      
      {/* Tag filters */}
      <div className="tag-filters">
        {['finance', 'gen-z', 'investing', 'markets', '2024'].map(tag => (
          <button
            key={tag}
            className={selectedTags.includes(tag) ? 'active' : ''}
            onClick={() => {
              const newTags = selectedTags.includes(tag)
                ? selectedTags.filter(t => t !== tag)
                : [...selectedTags, tag];
              handleTagFilter(newTags);
            }}
          >
            {tag}
          </button>
        ))}
      </div>
      
      {/* Documents */}
      <div className="documents-list">
        {documents.map(doc => (
          <div 
            key={doc.id} 
            className={`document-card ${doc.selected ? 'selected' : ''}`}
            onClick={() => handleDocumentToggle(doc.id)}
          >
            <h4>{doc.title}</h4>
            <p>{doc.description}</p>
            <div className="document-meta">
              <span className="date">{doc.date}</span>
              <span className="category">{doc.category}</span>
            </div>
            <div className="tags">
              {doc.tags.map(tag => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="selection-summary">
        Selected: {documents.filter(d => d.selected).length} contents
      </div>
    </div>
  );
};

export default KnowledgeBaseSelector;
```

### **4. Integrazione con Form di Generazione**

```jsx
const ContentGenerationForm = () => {
  const [selectedDocuments, setSelectedDocuments] = useState([]);
  const [formData, setFormData] = useState({
    topic: '',
    contentType: 'article',
    clientProfile: 'siebert',
    // ... altri campi
  });

  const handleDocumentsChange = (documents) => {
    const selected = documents.filter(doc => doc.selected);
    setSelectedDocuments(selected);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = {
      ...formData,
      selectedDocuments: selectedDocuments.map(doc => doc.id),
      // Il backend userà questi ID per recuperare il contenuto specifico
    };
    
    try {
      const response = await fetch('/api/v1/content/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      // Handle response...
    } catch (error) {
      console.error('Generation error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Altri campi del form */}
      
      <KnowledgeBaseSelector 
        clientName={formData.clientProfile}
        onDocumentsChange={handleDocumentsChange}
      />
      
      <button type="submit" disabled={selectedDocuments.length === 0}>
        Generate Content
      </button>
    </form>
  );
};
```

## 🔧 API Endpoints Disponibili

### **1. Get Frontend Documents**
```
GET /api/v1/knowledge-base/frontend/clients/{client_name}/documents
```

**Query Parameters:**
- `search` (optional): Search query
- `tags` (optional): Filter by tags (can be multiple)

**Response:** Array of frontend-compatible documents

### **2. Get Document Content**
```
GET /api/v1/knowledge-base/clients/{client_name}/documents/{document_id}
```

**Response:** Full document content with metadata

### **3. Get Available Clients**
```
GET /api/v1/knowledge-base/clients
```

**Response:** Array of client names

## 🎯 Benefici dell'Integrazione

1. **📚 Contenuti Reali**: Documenti effettivi dalla knowledge base
2. **🔍 Search & Filter**: Ricerca e filtri funzionanti
3. **🏷️ Tag Automatici**: Tag estratti automaticamente dal contenuto
4. **📊 Metadata Reali**: Date, dimensioni, categorie reali
5. **🔄 Sincronizzazione**: Sempre aggiornato con i file su disco

## 🚀 Prossimi Passi

1. **Sostituire Mock Data**: Implementare le chiamate API reali
2. **Error Handling**: Gestire errori di rete e stati di loading
3. **Caching**: Implementare cache per migliorare performance
4. **Real-time Updates**: WebSocket per aggiornamenti in tempo reale
5. **Upload Interface**: Interfaccia per caricare nuovi documenti

## 📝 Note Tecniche

- **CORS**: Assicurarsi che il backend abbia CORS configurato per il frontend
- **Authentication**: Aggiungere autenticazione se necessario
- **Rate Limiting**: Implementare rate limiting per le API
- **Validation**: Validare i dati ricevuti dal backend
