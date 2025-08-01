import axios from 'axios';
import {
  ClientProfile,
  WorkflowType,
  RAGContent,
  GenerationRequest,
  GenerationResponse,
  SystemInfo,
  ApiResponse
} from '../types';

// Configure axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
  timeout: 120000, // Increased to 2 minutes for content generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // System endpoints
  async getSystemInfo(): Promise<SystemInfo> {
    const response = await api.get<SystemInfo>('/api/v1/system/info');
    return response.data;
  },

  async getHealth(): Promise<any> {
    const response = await api.get('/health');
    return response.data;
  },

  // Client profiles endpoints
  async getClientProfiles(): Promise<ClientProfile[]> {
    // For now, return mock data - will be replaced with real API
    return [
      {
        id: 'siebert',
        name: 'siebert',
        displayName: 'Siebert Financial',
        description: 'Financial services company focused on empowering individual investors',
        brandVoice: 'Professional yet accessible, empowering, educational, trustworthy',
        targetAudience: 'Gen Z and young professionals interested in financial literacy',
        industry: 'Financial Services',
        ragEnabled: true,
        knowledgeBasePath: 'data/knowledge_base/siebert'
      },
      {
        id: 'default',
        name: 'default',
        displayName: 'Default Profile',
        description: 'General purpose content generation profile',
        brandVoice: 'Professional and informative',
        targetAudience: 'General audience',
        industry: 'General',
        ragEnabled: false
      }
    ];
  },

  // Workflow endpoints
  async getWorkflowTypes(): Promise<WorkflowType[]> {
    // Mock data for now - will be replaced with real API
    return [
      {
        id: 'enhanced_article',
        name: 'enhanced_article',
        displayName: 'Enhanced Article',
        description: 'Comprehensive article with research, analysis, and expert insights',
        category: 'article',
        requiredFields: [
          {
            id: 'topic',
            name: 'topic',
            label: 'Article Topic',
            type: 'text',
            required: true,
            placeholder: 'Enter the main topic for your article'
          },
          {
            id: 'target_word_count',
            name: 'target_word_count',
            label: 'Target Word Count',
            type: 'number',
            required: true,
            validation: { min: 500, max: 3000 }
          }
        ],
        optionalFields: [
          {
            id: 'tone',
            name: 'tone',
            label: 'Tone',
            type: 'select',
            required: false,
            options: [
              { value: 'professional', label: 'Professional' },
              { value: 'conversational', label: 'Conversational' },
              { value: 'academic', label: 'Academic' },
              { value: 'casual', label: 'Casual' }
            ]
          },
          {
            id: 'include_statistics',
            name: 'include_statistics',
            label: 'Include Statistics',
            type: 'boolean',
            required: false
          }
        ]
      },
      {
        id: 'premium_newsletter',
        name: 'premium_newsletter',
        displayName: 'Premium Newsletter',
        description: 'Advanced newsletter with premium source analysis and client-specific brand integration',
        category: 'newsletter',
        requiredFields: [
          {
            id: 'newsletter_topic',
            name: 'newsletter_topic',
            label: 'Newsletter Topic',
            type: 'textarea',
            required: true,
            placeholder: 'Enter the main theme for this newsletter edition',
            validation: { min: 5, max: 200 }
          },
          {
            id: 'premium_sources',
            name: 'premium_sources',
            label: 'Premium Sources URLs',
            type: 'text',
            required: true,
            placeholder: 'Enter premium source URLs (one per line, max 10)',
            validation: { min: 1, max: 10 }
          },
          {
            id: 'target_audience',
            name: 'target_audience',
            label: 'Target Audience',
            type: 'textarea',
            required: true,
            placeholder: 'Describe the specific target audience for this edition',
            validation: { min: 3, max: 500 }
          }
        ],
        optionalFields: [
          {
            id: 'target_word_count',
            name: 'target_word_count',
            label: 'Target Word Count',
            type: 'number',
            required: false,
            placeholder: '1200',
            validation: { min: 800, max: 2500 }
          },
          {
            id: 'edition_number',
            name: 'edition_number',
            label: 'Edition Number',
            type: 'number',
            required: false,
            placeholder: '1'
          },
          {
            id: 'exclude_topics',
            name: 'exclude_topics',
            label: 'Topics to Exclude',
            type: 'text',
            required: false,
            placeholder: 'Enter topics to exclude (comma-separated)'
          },
          {
            id: 'priority_sections',
            name: 'priority_sections',
            label: 'Priority Sections',
            type: 'text',
            required: false,
            placeholder: 'Enter priority sections (comma-separated)'
          },
          {
            id: 'custom_instructions',
            name: 'custom_instructions',
            label: 'Custom Instructions',
            type: 'textarea',
            required: false,
            placeholder: 'Any additional instructions for the newsletter generation'
          }
        ]
      }
    ];
  },

  // RAG content endpoints
  async getRAGContents(clientProfile: string): Promise<RAGContent[]> {
    try {
      console.log(`🔍 Fetching RAG contents for client: ${clientProfile}`);

      // Call real knowledge base API
      const response = await api.get(`/api/v1/knowledge-base/frontend/clients/${clientProfile}/documents`);

      console.log(`✅ Received ${response.data.length} documents from knowledge base`);

      // Transform backend format to frontend format
      const ragContents: RAGContent[] = response.data.map((doc: any) => ({
        id: doc.id,
        title: doc.title,
        content: doc.description, // Use description as preview content
        type: doc.category,
        clientProfile: clientProfile,
        tags: doc.tags,
        createdAt: doc.date + 'T00:00:00Z', // Convert date to ISO format
        score: 1.0 // Default score
      }));

      return ragContents;

    } catch (error) {
      console.error(`❌ Error fetching RAG contents for ${clientProfile}:`, error);

      // Fallback to mock data if API fails
      console.log('🔄 Falling back to mock data');
      if (clientProfile === 'siebert') {
        return [
          {
            id: 'rag_1',
            title: 'Financial Market Trends 2024',
            content: 'Comprehensive analysis of current market trends...',
            type: 'market_analysis',
            clientProfile: 'siebert',
            tags: ['finance', 'markets', '2024'],
            createdAt: '2024-01-15T10:00:00Z'
          },
          {
            id: 'rag_2',
            title: 'Gen Z Investment Preferences',
            content: 'Research on how Gen Z approaches investing...',
            type: 'research',
            clientProfile: 'siebert',
            tags: ['gen-z', 'investing', 'preferences'],
            createdAt: '2024-01-10T14:30:00Z'
          }
        ];
      }
      return [];
    }
  },

  // Get specific RAG document content
  async getRAGDocumentContent(clientProfile: string, documentId: string): Promise<string> {
    try {
      console.log(`📄 Fetching document content: ${clientProfile}/${documentId}`);

      const response = await api.get(`/api/v1/knowledge-base/clients/${clientProfile}/documents/${documentId}`);

      console.log(`✅ Retrieved document content (${response.data.content.length} chars)`);

      return response.data.content;

    } catch (error) {
      console.error(`❌ Error fetching document content ${clientProfile}/${documentId}:`, error);
      throw error;
    }
  },

  // Get available clients from knowledge base
  async getAvailableClients(): Promise<string[]> {
    try {
      console.log('📋 Fetching available clients from knowledge base');

      const response = await api.get('/api/v1/knowledge-base/clients');

      console.log(`✅ Found ${response.data.length} clients:`, response.data);

      return response.data;

    } catch (error) {
      console.error('❌ Error fetching available clients:', error);
      // Fallback to default clients
      return ['siebert'];
    }
  },

  // Content generation endpoint
  async generateContent(request: GenerationRequest): Promise<GenerationResponse> {
    console.log('🚀 Starting content generation with request:', request);

    const payload = {
      topic: request.parameters.topic || request.parameters.newsletter_topic,
      content_type: request.workflowType === 'newsletter_premium' ? 'newsletter' : 'article',
      content_format: 'markdown',
      client_profile: request.clientProfile,
      workflow_type: request.workflowType,
      selected_documents: request.ragContentIds || [], // Pass selected RAG content IDs
      ...request.parameters
    };

    console.log('📤 Sending payload to backend:', payload);

    try {
      const response = await api.post<any>('/api/v1/content/generate', payload, {
        timeout: 180000 // 3 minutes for content generation specifically
      });

      console.log('✅ Content generation successful:', response.data);

      // Transform backend response to frontend format
      const result: GenerationResponse = {
        contentId: response.data.content_id || response.data.contentId || 'unknown',
        title: response.data.title || 'Generated Content',
        body: response.data.content || response.data.body || '',
        contentType: response.data.content_type || response.data.contentType || 'article',
        wordCount: response.data.word_count || response.data.wordCount || 0,
        generationTime: response.data.generation_time_seconds || response.data.generationTime || 0,
        success: true
      };

      return result;

    } catch (error) {
      console.error('❌ Content generation failed:', error);
      throw error;
    }
  }
};

export default apiService;
