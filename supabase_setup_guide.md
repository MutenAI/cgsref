# 🚀 Supabase Setup Guide for CGSRef

## 📋 Quick Setup Checklist

### 1. 🏗️ Create Supabase Project
- [ ] Go to [supabase.com](https://supabase.com)
- [ ] Create new account/login
- [ ] Create new project: `cgsref-production`
- [ ] Choose region (closest to your users)
- [ ] Set strong database password
- [ ] Wait for project initialization (~2 minutes)

### 2. 📊 Database Setup
- [ ] Go to SQL Editor in Supabase dashboard
- [ ] Copy and paste `supabase_schema.sql`
- [ ] Run the schema creation script
- [ ] Verify tables are created in Table Editor

### 3. 🔐 Authentication Configuration
- [ ] Go to Authentication > Settings
- [ ] Configure Site URL: `http://localhost:3001` (development)
- [ ] Add production URL when ready
- [ ] Enable email confirmation (recommended)
- [ ] Configure email templates (optional)

### 4. 📁 Storage Setup
- [ ] Go to Storage section
- [ ] Create bucket: `knowledge-base`
- [ ] Set bucket to public (for document access)
- [ ] Create bucket: `generated-content` (private)
- [ ] Configure CORS if needed

### 5. 🔑 API Keys
- [ ] Go to Settings > API
- [ ] Copy `anon` key (for frontend)
- [ ] Copy `service_role` key (for backend)
- [ ] Copy project URL
- [ ] Store in environment variables

## 🛠️ Environment Variables

### Frontend (.env.local)
```bash
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
REACT_APP_API_URL=http://localhost:8001  # Your AI backend
```

### Backend (.env)
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key

# AI Service Keys
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
DEEPSEEK_API_KEY=your-deepseek-key
SERPER_API_KEY=your-serper-key
```

## 📱 Frontend Integration

### Install Supabase Client
```bash
cd web/react-app
npm install @supabase/supabase-js
```

### Create Supabase Client
```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL!
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### Update API Service
```typescript
// src/services/supabaseApi.ts
import { supabase } from '../lib/supabase'

export const supabaseApi = {
  // Get documents for client
  async getDocuments(clientName: string) {
    const { data, error } = await supabase
      .from('documents')
      .select(`
        id,
        title,
        description,
        category,
        tags,
        created_at,
        clients!inner(name)
      `)
      .eq('clients.name', clientName)
    
    if (error) throw error
    return data
  },

  // Create content generation
  async createGeneration(generation: any) {
    const { data, error } = await supabase
      .from('content_generations')
      .insert(generation)
      .select()
      .single()
    
    if (error) throw error
    return data
  },

  // Get user generations
  async getUserGenerations() {
    const { data, error } = await supabase
      .from('content_generations')
      .select(`
        id,
        title,
        content_type,
        status,
        created_at,
        clients(name, display_name)
      `)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  }
}
```

## 🤖 Backend Integration

### Install Supabase Python Client
```bash
pip install supabase
```

### Create Supabase Client
```python
# core/infrastructure/external_services/supabase_client.py
import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

class SupabaseClient:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        self.client: Client = create_client(url, key)
    
    async def get_client_documents(self, client_name: str) -> List[Dict[str, Any]]:
        """Get all documents for a client"""
        response = (
            self.client
            .table('documents')
            .select('*, clients!inner(name)')
            .eq('clients.name', client_name)
            .execute()
        )
        return response.data
    
    async def save_generation(self, generation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save content generation result"""
        response = (
            self.client
            .table('content_generations')
            .insert(generation_data)
            .execute()
        )
        return response.data[0]
    
    async def update_generation_status(self, generation_id: str, status: str, **kwargs):
        """Update generation status"""
        update_data = {"status": status, **kwargs}
        response = (
            self.client
            .table('content_generations')
            .update(update_data)
            .eq('id', generation_id)
            .execute()
        )
        return response.data[0]
```

## 🔄 Real-time Updates

### Frontend Real-time Subscriptions
```typescript
// Listen for generation updates
useEffect(() => {
  const subscription = supabase
    .channel('content_generations')
    .on(
      'postgres_changes',
      {
        event: 'UPDATE',
        schema: 'public',
        table: 'content_generations',
        filter: `created_by=eq.${user.id}`
      },
      (payload) => {
        // Update UI when generation status changes
        setGenerations(prev => 
          prev.map(gen => 
            gen.id === payload.new.id ? payload.new : gen
          )
        )
      }
    )
    .subscribe()

  return () => {
    subscription.unsubscribe()
  }
}, [user.id])
```

## 📁 File Upload to Storage

### Upload Knowledge Base Documents
```typescript
// Upload document to Supabase Storage
async function uploadDocument(file: File, clientName: string) {
  const fileName = `${clientName}/${Date.now()}-${file.name}`
  
  const { data, error } = await supabase.storage
    .from('knowledge-base')
    .upload(fileName, file)
  
  if (error) throw error
  
  // Save metadata to database
  const { data: docData, error: docError } = await supabase
    .from('documents')
    .insert({
      title: file.name,
      file_path: data.path,
      file_size: file.size,
      file_type: file.type,
      client_id: clientId
    })
  
  if (docError) throw docError
  return docData
}
```

## 🔐 Security Best Practices

### Row Level Security Policies
- ✅ Users can only see their own generations
- ✅ Documents are readable by all authenticated users
- ✅ API keys only accessible by admins
- ✅ User profiles are private

### API Key Management
```sql
-- Encrypt API keys before storing
INSERT INTO api_keys (service_name, key_name, encrypted_key) 
VALUES ('openai', 'main', crypt('your-api-key', gen_salt('bf')));

-- Decrypt when needed (in backend only)
SELECT decrypt(encrypted_key, 'your-encryption-key') 
FROM api_keys 
WHERE service_name = 'openai' AND key_name = 'main';
```

## 🚀 Deployment Strategy

### Development
- Frontend: `npm run dev` (localhost:3001)
- Backend: `python start_backend.py` (localhost:8001)
- Database: Supabase cloud

### Production
- Frontend: Vercel (auto-deploy from GitHub)
- Backend: Railway/Render (Docker deployment)
- Database: Supabase cloud (same instance)

## 📊 Monitoring and Analytics

### Supabase Dashboard
- Real-time database activity
- API usage statistics
- Storage usage
- Authentication metrics

### Custom Analytics
```sql
-- Track generation statistics
SELECT 
  DATE(created_at) as date,
  COUNT(*) as total_generations,
  AVG(generation_time_seconds) as avg_time,
  SUM(cost_usd) as total_cost
FROM content_generations 
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## 🔧 Migration from Current System

### 1. Data Migration
- [ ] Export current knowledge base documents
- [ ] Upload to Supabase Storage
- [ ] Create document records in database
- [ ] Migrate user data (if any)

### 2. Code Migration
- [ ] Update frontend to use Supabase client
- [ ] Modify backend to use Supabase for persistence
- [ ] Keep AI processing logic unchanged
- [ ] Update environment variables

### 3. Testing
- [ ] Test authentication flow
- [ ] Test document upload/retrieval
- [ ] Test content generation end-to-end
- [ ] Test real-time updates

## 🎯 Next Steps

1. **Create Supabase project** and run schema
2. **Update frontend** to use Supabase auth
3. **Migrate knowledge base** to Supabase Storage
4. **Deploy to Vercel** for frontend
5. **Deploy backend** to Railway/Render
6. **Configure custom domain** and SSL
