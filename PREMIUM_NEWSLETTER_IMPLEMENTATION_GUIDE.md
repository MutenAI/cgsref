# 🚀 Premium Newsletter Workflow - Implementation Guide

**Date**: 2025-07-27  
**Target Workflow**: `premium_newsletter`  
**Safety Level**: PRODUCTION-SAFE  
**Implementation Type**: ADDITIVE ONLY

---

## ⚠️ CRITICAL SAFETY CONSTRAINTS

### 🔒 **ABSOLUTE RESTRICTIONS - DO NOT MODIFY**
```
❌ NEVER TOUCH THESE FILES:
- core/infrastructure/workflows/handlers/enhanced_article_handler.py
- core/infrastructure/workflows/templates/enhanced_article.json
- api/rest/v1/endpoints/content.py (content generation endpoint)
- api/rest/main.py (main API router)
- Any existing agent files
- Any existing tool files
- Database migration files
```

### ✅ **SAFE MODIFICATION ZONES**
```
✅ SAFE TO MODIFY:
- core/infrastructure/workflows/handlers/__init__.py (ADD imports only)
- core/infrastructure/workflows/__init__.py (ADD imports only)
- web/react-app/src/services/api.ts (ADD workflow config only)
- web/react-app/src/components/WorkflowForm.tsx (ADD form logic only)
```

### 🛡️ **SAFETY PRINCIPLES**
1. **ADDITIVE ONLY**: Only add new code, never modify existing functionality
2. **ISOLATED IMPLEMENTATION**: New workflow must be completely independent
3. **BACKWARD COMPATIBILITY**: Existing workflows must continue working unchanged
4. **INCREMENTAL TESTING**: Test after each major component addition
5. **ROLLBACK READY**: Each step must be easily reversible

---

## 📋 IMPLEMENTATION CHECKLIST

### **PHASE 1: Backend Foundation** ⏱️ ~2 hours

#### ✅ **Step 1.1: Create Premium Newsletter Handler**
- [ ] **File**: `core/infrastructure/workflows/handlers/premium_newsletter_handler.py`
- [ ] **Action**: Create new file (DO NOT modify existing handlers)
- [ ] **Content**: Complete handler class with all required methods
- [ ] **Validation**: Import test - `python -c "from core.infrastructure.workflows.handlers.premium_newsletter_handler import PremiumNewsletterHandler; print('✅ Handler created successfully')"`

#### ✅ **Step 1.2: Create Workflow Template**
- [ ] **File**: `core/infrastructure/workflows/templates/premium_newsletter.json`
- [ ] **Action**: Create new JSON template file
- [ ] **Content**: Complete workflow definition with 3 tasks
- [ ] **Validation**: JSON syntax check - `python -c "import json; json.load(open('core/infrastructure/workflows/templates/premium_newsletter.json')); print('✅ Template valid')"`

#### ✅ **Step 1.3: Register Handler (SAFE ADDITION)**
- [ ] **File**: `core/infrastructure/workflows/handlers/__init__.py`
- [ ] **Action**: ADD import line only (do not remove existing imports)
- [ ] **Add**: `from .premium_newsletter_handler import PremiumNewsletterHandler`
- [ ] **Add**: `PremiumNewsletterHandler` to `__all__` list
- [ ] **Validation**: Import test - `python -c "from core.infrastructure.workflows.handlers import PremiumNewsletterHandler; print('✅ Handler registered')"`

#### ✅ **Step 1.4: Register in Main Workflows Module (SAFE ADDITION)**
- [ ] **File**: `core/infrastructure/workflows/__init__.py`
- [ ] **Action**: ADD import line only (do not remove existing imports)
- [ ] **Add**: `from .handlers.premium_newsletter_handler import PremiumNewsletterHandler`
- [ ] **Add**: `PremiumNewsletterHandler` to `__all__` list
- [ ] **Validation**: Registry test - `python -c "from core.infrastructure.workflows.registry import list_available_workflows; print('Available:', list_available_workflows())"`

#### ✅ **Step 1.5: Verify Backend Integration**
- [ ] **Test**: Start backend server - `python -m uvicorn api.rest.main:app --reload --port 8001`
- [ ] **Test**: Check workflow registration - `curl http://localhost:8001/api/v1/workflows/`
- [ ] **Test**: Verify enhanced_article still works - Test existing workflow
- [ ] **Expected**: Both `enhanced_article` and `premium_newsletter` should appear in workflow list

---

### **PHASE 2: Frontend Integration** ⏱️ ~1.5 hours

#### ✅ **Step 2.1: Add Workflow Configuration (SAFE ADDITION)**
- [ ] **File**: `web/react-app/src/services/api.ts`
- [ ] **Action**: ADD new workflow object to `getWorkflowTypes()` array
- [ ] **Location**: Add after existing `enhanced_article` configuration
- [ ] **Content**: Complete premium_newsletter configuration with all fields
- [ ] **Validation**: TypeScript compilation - `cd web/react-app && npm run build`

#### ✅ **Step 2.2: Add Form Schema (SAFE ADDITION)**
- [ ] **File**: `web/react-app/src/components/WorkflowForm.tsx`
- [ ] **Action**: ADD new schema after existing schemas (line ~82)
- [ ] **Add**: `premiumNewsletterSchema` with Yup validation
- [ ] **Add**: `PremiumNewsletterFormData` type definition
- [ ] **Validation**: TypeScript compilation check

#### ✅ **Step 2.3: Add Form Logic (SAFE ADDITION)**
- [ ] **File**: `web/react-app/src/components/WorkflowForm.tsx`
- [ ] **Action**: ADD new case in `getValidationSchema()` function
- [ ] **Add**: `if (selectedWorkflow?.id === 'premium_newsletter') return premiumNewsletterSchema;`
- [ ] **Action**: ADD new case in `getDefaultValues()` function
- [ ] **Add**: Default values for premium_newsletter fields
- [ ] **Validation**: Form logic test

#### ✅ **Step 2.4: Add Form Rendering (SAFE ADDITION)**
- [ ] **File**: `web/react-app/src/components/WorkflowForm.tsx`
- [ ] **Action**: ADD new render function `renderPremiumNewsletterForm()`
- [ ] **Location**: After existing render functions (around line 500)
- [ ] **Action**: ADD conditional rendering in return statement
- [ ] **Add**: `{selectedWorkflow.id === 'premium_newsletter' && renderPremiumNewsletterForm()}`
- [ ] **Validation**: UI rendering test

#### ✅ **Step 2.5: Verify Frontend Integration**
- [ ] **Test**: Start frontend - `cd web/react-app && npm start`
- [ ] **Test**: Navigate to workflow selection
- [ ] **Test**: Verify premium_newsletter appears in workflow list
- [ ] **Test**: Verify enhanced_article still works correctly
- [ ] **Test**: Select premium_newsletter and verify form renders

---

### **PHASE 3: Advanced Components (OPTIONAL)** ⏱️ ~3 hours

#### ✅ **Step 3.1: Create Premium Sources Analyzer (OPTIONAL)**
- [ ] **File**: `core/infrastructure/agents/premium_sources_analyzer.py`
- [ ] **Action**: Create new agent file (completely independent)
- [ ] **Content**: Specialized agent for premium source analysis
- [ ] **Validation**: Agent import test

#### ✅ **Step 3.2: Create Premium Financial Sources Tool (OPTIONAL)**
- [ ] **File**: `core/infrastructure/tools/premium_financial_sources_tool.py`
- [ ] **Action**: Create new tool file (completely independent)
- [ ] **Content**: Advanced content extraction tool
- [ ] **Validation**: Tool import test

#### ✅ **Step 3.3: Create Custom UI Components (OPTIONAL)**
- [ ] **File**: `web/react-app/src/components/common/URLArrayInput.tsx`
- [ ] **Action**: Create new UI component for URL array management
- [ ] **File**: `web/react-app/src/components/common/TagArrayInput.tsx`
- [ ] **Action**: Create new UI component for tag array management
- [ ] **Validation**: Component rendering test

---

### **PHASE 4: Testing & Validation** ⏱️ ~1 hour

#### ✅ **Step 4.1: Backend Validation**
- [ ] **Test**: Server startup without errors
- [ ] **Test**: Workflow registry includes both workflows
- [ ] **Test**: Enhanced article workflow still functional
- [ ] **Test**: Premium newsletter workflow appears in API
- [ ] **Test**: No import errors or conflicts

#### ✅ **Step 4.2: Frontend Validation**
- [ ] **Test**: Application compiles and starts
- [ ] **Test**: Workflow selector shows both options
- [ ] **Test**: Enhanced article form still works
- [ ] **Test**: Premium newsletter form renders correctly
- [ ] **Test**: Form validation works for both workflows

#### ✅ **Step 4.3: End-to-End Validation**
- [ ] **Test**: Generate content with enhanced_article (verify no regression)
- [ ] **Test**: Select premium_newsletter workflow
- [ ] **Test**: Fill out premium newsletter form
- [ ] **Test**: Submit form (may fail gracefully if agents/tools not implemented)
- [ ] **Test**: System remains stable after all operations

---

## 📁 FILE MODIFICATION MATRIX

### **NEW FILES TO CREATE** ✅
```
📁 Backend Files (2 required + 2 optional):
├── core/infrastructure/workflows/handlers/premium_newsletter_handler.py ✅ REQUIRED
├── core/infrastructure/workflows/templates/premium_newsletter.json ✅ REQUIRED
├── core/infrastructure/agents/premium_sources_analyzer.py ⚪ OPTIONAL
└── core/infrastructure/tools/premium_financial_sources_tool.py ⚪ OPTIONAL

📁 Frontend Files (2 optional):
├── web/react-app/src/components/common/URLArrayInput.tsx ⚪ OPTIONAL
└── web/react-app/src/components/common/TagArrayInput.tsx ⚪ OPTIONAL
```

### **EXISTING FILES TO MODIFY** ⚠️
```
📝 Backend Modifications (ADDITIVE ONLY):
├── core/infrastructure/workflows/handlers/__init__.py
│   └── ADD: from .premium_newsletter_handler import PremiumNewsletterHandler
│   └── ADD: 'PremiumNewsletterHandler' to __all__
└── core/infrastructure/workflows/__init__.py
    └── ADD: from .handlers.premium_newsletter_handler import PremiumNewsletterHandler
    └── ADD: 'PremiumNewsletterHandler' to __all__

📝 Frontend Modifications (ADDITIVE ONLY):
├── web/react-app/src/services/api.ts
│   └── ADD: premium_newsletter configuration to getWorkflowTypes()
└── web/react-app/src/components/WorkflowForm.tsx
    ├── ADD: premiumNewsletterSchema
    ├── ADD: PremiumNewsletterFormData type
    ├── ADD: case in getValidationSchema()
    ├── ADD: case in getDefaultValues()
    ├── ADD: renderPremiumNewsletterForm() function
    └── ADD: conditional rendering in return statement
```

### **FILES TO NEVER TOUCH** ❌
```
🚫 PROTECTED FILES:
├── core/infrastructure/workflows/handlers/enhanced_article_handler.py
├── core/infrastructure/workflows/templates/enhanced_article.json
├── api/rest/v1/endpoints/content.py
├── api/rest/main.py
├── core/infrastructure/agents/ (existing agents)
├── core/infrastructure/tools/ (existing tools)
└── Any database or migration files
```

---

## 🛡️ SAFETY GUIDELINES

### **🔍 Pre-Implementation Checks**
1. **Backup Current State**: Create git commit before starting
2. **Verify System Health**: Ensure enhanced_article workflow works
3. **Check Dependencies**: Verify all required packages are installed
4. **Test Environment**: Confirm development environment is stable

### **⚡ During Implementation**
1. **One Phase at a Time**: Complete each phase before moving to next
2. **Test After Each Step**: Verify system stability after major changes
3. **Additive Only**: Never modify existing code, only add new code
4. **Import Safety**: Always add imports, never remove or modify existing ones

### **🧪 Validation Requirements**
1. **After Each Phase**: Run validation tests specified in checklist
2. **Before Moving Forward**: Ensure previous phase is fully working
3. **Regression Testing**: Verify enhanced_article still works after each change
4. **Error Handling**: Any errors should not affect existing functionality

### **🔄 Rollback Procedures**
1. **Git Rollback**: `git checkout -- <filename>` for individual files
2. **Full Rollback**: `git reset --hard HEAD~1` to undo last commit
3. **Selective Rollback**: Remove only new files, restore modified files
4. **Verification**: Test enhanced_article workflow after rollback

---

## 📋 DETAILED TECHNICAL SPECIFICATIONS

### **🔧 Premium Newsletter Handler Template**

**File**: `core/infrastructure/workflows/handlers/premium_newsletter_handler.py`

```python
"""
Premium Newsletter workflow handler.
"""

import logging
from typing import Dict, Any, List

from ..base.workflow_base import WorkflowHandler
from ..registry import register_workflow

logger = logging.getLogger(__name__)

@register_workflow('premium_newsletter')
class PremiumNewsletterHandler(WorkflowHandler):
    """Handler for premium newsletter workflow."""

    def validate_inputs(self, context: Dict[str, Any]) -> None:
        """Validate inputs specific to premium newsletter."""
        super().validate_inputs(context)

        # Validate newsletter_topic
        topic = context.get('newsletter_topic', '')
        if not topic or len(topic) < 5:
            raise ValueError("Newsletter topic must be at least 5 characters")
        if len(topic) > 200:
            raise ValueError("Newsletter topic must be less than 200 characters")

        # Validate premium_sources
        sources = context.get('premium_sources', [])
        if not sources or len(sources) < 1:
            raise ValueError("At least one premium source is required")
        if len(sources) > 10:
            raise ValueError("Maximum 10 premium sources allowed")

        # Validate URLs
        for source in sources:
            if not source.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid URL format: {source}")

        # Validate target_audience
        audience = context.get('target_audience', '')
        if not audience or len(audience) < 3:
            raise ValueError("Target audience must be at least 3 characters")
        if len(audience) > 500:
            raise ValueError("Target audience must be less than 500 characters")

        # Validate target_word_count
        word_count = context.get('target_word_count', 1200)
        if word_count < 800 or word_count > 2500:
            raise ValueError("Target word count must be between 800 and 2500")

        logger.info(f"✅ Premium newsletter inputs validated: {len(sources)} sources, {word_count} words target")

    def prepare_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare context for premium newsletter."""
        context = super().prepare_context(context)

        # Set default values
        context.setdefault('target_word_count', 1200)
        context.setdefault('edition_number', 1)
        context.setdefault('exclude_topics', [])
        context.setdefault('priority_sections', [])
        context.setdefault('custom_instructions', '')

        # Calculate word count distribution for 7 sections
        total_words = context['target_word_count']
        context['section_word_counts'] = {
            'executive_summary': int(total_words * 0.15),
            'market_highlights': int(total_words * 0.20),
            'premium_insights': int(total_words * 0.25),
            'expert_analysis': int(total_words * 0.15),
            'recommendations': int(total_words * 0.15),
            'market_outlook': int(total_words * 0.07),
            'client_cta': int(total_words * 0.03)
        }

        # Sanitize and validate URLs
        sources = context.get('premium_sources', [])
        context['premium_sources'] = [url.strip() for url in sources if url.strip()]

        logger.info(f"🔧 Premium newsletter context prepared: {len(context['premium_sources'])} sources")
        logger.info(f"📊 Section word counts: {context['section_word_counts']}")

        return context

    def post_process_task(self, task_id: str, task_output: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process task output."""
        logger.info(f"🔧 POST-PROCESSING TASK: {task_id}")

        if task_id == 'task1_enhanced_context':
            # Extract brand guidelines and structure requirements
            context['brand_guidelines_extracted'] = True
            logger.info(f"📋 Brand guidelines extracted for {context.get('client_name', 'client')}")

        elif task_id == 'task2_premium_analysis':
            # Validate premium content extraction
            sources_count = len(context.get('premium_sources', []))
            context['premium_sources_analyzed'] = sources_count
            logger.info(f"📊 Premium sources analyzed: {sources_count}")

        elif task_id == 'task3_newsletter_creation':
            # Verify newsletter structure and word counts
            word_count = len(task_output.split()) if task_output else 0
            context['final_word_count'] = word_count
            target_count = context.get('target_word_count', 1200)
            accuracy = (word_count / target_count * 100) if target_count > 0 else 0
            context['word_count_accuracy'] = accuracy
            logger.info(f"📄 Newsletter created: {word_count} words ({accuracy:.1f}% of target)")

        return context

    def post_process_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Final post-processing with newsletter-specific metrics."""
        try:
            logger.info("🔧 POST-PROCESSING: Starting premium newsletter post-processing")

            # Find the final newsletter content
            final_content = None
            task_outputs = []

            for key, value in context.items():
                if key.endswith('_output') and isinstance(value, str):
                    task_outputs.append((key, value, len(value)))
                    logger.info(f"📊 Found task output: {key} ({len(value)} chars)")

            # Prioritize task3_newsletter_creation output
            if task_outputs:
                task3_output = None
                for key, value, length in task_outputs:
                    if key == 'task3_newsletter_creation_output':
                        task3_output = (key, value, length)
                        break

                if task3_output:
                    final_content = task3_output[1]
                    logger.info(f"📄 Selected newsletter content from {task3_output[0]} ({task3_output[2]} chars)")
                else:
                    # Fallback to longest output
                    task_outputs.sort(key=lambda x: x[2], reverse=True)
                    final_content = task_outputs[0][1]
                    logger.info(f"📄 Selected content from {task_outputs[0][0]} ({task_outputs[0][2]} chars) - fallback")

            if final_content:
                context['final_output'] = final_content
                logger.info(f"📄 Set final_output with {len(final_content)} characters")

            # Create workflow summary with newsletter-specific metrics
            summary = {
                'workflow_type': 'premium_newsletter',
                'newsletter_topic': context.get('newsletter_topic', ''),
                'client': context.get('client_name', ''),
                'target_audience': context.get('target_audience', ''),
                'edition_number': context.get('edition_number', 1),
                'premium_sources_count': len(context.get('premium_sources', [])),
                'target_word_count': context.get('target_word_count', 1200),
                'final_word_count': context.get('final_word_count', 0),
                'word_count_accuracy': context.get('word_count_accuracy', 0),
                'sections_structure': '7-section newsletter',
                'brand_guidelines_applied': context.get('brand_guidelines_extracted', False),
                'premium_analysis_completed': context.get('premium_sources_analyzed', 0) > 0,
                'quality_indicators': {
                    'sources_analyzed': context.get('premium_sources_analyzed', 0),
                    'word_count_target_met': abs(context.get('word_count_accuracy', 0) - 100) <= 10,
                    'brand_integration': context.get('brand_guidelines_extracted', False)
                }
            }

            context['workflow_summary'] = summary
            logger.info(f"📊 Premium newsletter workflow summary created")
            logger.info(f"🎯 Word count accuracy: {summary['word_count_accuracy']:.1f}%")

            return context

        except Exception as e:
            logger.error(f"❌ POST-PROCESSING ERROR: {str(e)}")
            return context
```

### **📄 Premium Newsletter Template**

**File**: `core/infrastructure/workflows/templates/premium_newsletter.json`

```json
{
  "name": "premium_newsletter",
  "version": "1.0",
  "description": "Premium newsletter generation with advanced source analysis and client-specific brand integration",
  "handler": "premium_newsletter_handler",
  "variables": [
    {
      "name": "newsletter_topic",
      "type": "string",
      "required": true,
      "description": "Main theme for the newsletter edition"
    },
    {
      "name": "premium_sources",
      "type": "array",
      "required": true,
      "description": "Array of premium source URLs (max 10)"
    },
    {
      "name": "target_audience",
      "type": "string",
      "required": true,
      "description": "Specific target audience for this edition"
    },
    {
      "name": "target_word_count",
      "type": "integer",
      "required": false,
      "default": 1200,
      "description": "Total target word count for newsletter"
    },
    {
      "name": "edition_number",
      "type": "integer",
      "required": false,
      "default": 1,
      "description": "Newsletter edition number"
    },
    {
      "name": "exclude_topics",
      "type": "array",
      "required": false,
      "description": "Topics to exclude from analysis"
    },
    {
      "name": "priority_sections",
      "type": "array",
      "required": false,
      "description": "Newsletter sections to prioritize"
    },
    {
      "name": "custom_instructions",
      "type": "string",
      "required": false,
      "description": "Additional custom instructions"
    }
  ],
  "tasks": [
    {
      "id": "task1_enhanced_context",
      "name": "Enhanced Context & Brand Integration",
      "agent": "rag_specialist",
      "description_template": "TASK 1 - ENHANCED CONTEXT SETTING & BRAND INTEGRATION:\n\nOBJECTIVE:\nEstrai TUTTE le informazioni dalla knowledge base del cliente selezionato ({{client_name}}) e crea un brief operativo completo per la newsletter premium.\n\nSTEP 1: COMPREHENSIVE CLIENT ANALYSIS\nUtilizza il tool RAG per recuperare informazioni complete del cliente:\n[rag_get_client_content] {{client_name}} [/rag_get_client_content]\n\nSTEP 2: NEWSLETTER STRUCTURE DEFINITION\nAnalizza le informazioni recuperate e definisci:\n\nBRAND INTEGRATION:\n- Brand voice e tone specifici del cliente\n- Target audience primario e secondario\n- Messaggi chiave e value proposition\n- Terminologia e linguaggio preferiti\n- Call-to-action standard\n\nNEWSLETTER STRUCTURE (7 SEZIONI):\n1. Executive Summary ({{target_word_count * 0.15}} words)\n2. Market Highlights ({{target_word_count * 0.20}} words)\n3. Premium Insights ({{target_word_count * 0.25}} words)\n4. Expert Analysis ({{target_word_count * 0.15}} words)\n5. Actionable Recommendations ({{target_word_count * 0.15}} words)\n6. Market Outlook ({{target_word_count * 0.07}} words)\n7. Client-Specific CTA ({{target_word_count * 0.03}} words)\n\nCONTEXT REQUIREMENTS:\n- Newsletter Topic: {{newsletter_topic}}\n- Target Audience: {{target_audience}}\n- Edition Number: {{edition_number}}\n- Total Word Count: {{target_word_count}}\n- Exclude Topics: {{exclude_topics}}\n- Priority Sections: {{priority_sections}}\n\nOUTPUT:\nBrief operativo strutturato che servirà come guida per i task successivi, includendo word count precisi per ogni sezione e guidelines specifiche del cliente.",
      "dependencies": []
    },
    {
      "id": "task2_premium_analysis",
      "name": "Premium Sources Analysis & Content Extraction",
      "agent": "rag_specialist",
      "description_template": "TASK 2 - PREMIUM SOURCES ANALYSIS & CONTENT EXTRACTION:\n\nCONTEXT FROM PREVIOUS TASK:\n{{task1_enhanced_context_output}}\n\nOBJECTIVE:\nAnalizza le fonti premium fornite e estrai contenuti di alta qualità per alimentare la newsletter.\n\nINPUT SOURCES:\n{{premium_sources}}\n\nSTEP 1: SOURCE VALIDATION & PRIORITIZATION\nPer ogni URL nelle premium_sources:\n- Valida accessibilità e qualità della fonte\n- Classifica per rilevanza al topic: {{newsletter_topic}}\n- Identifica tipo di contenuto (news, analysis, data, reports)\n\nSTEP 2: PREMIUM CONTENT EXTRACTION\nUtilizza il tool web_search per ogni fonte:\n[web_search] site:{{premium_sources[0]}} {{newsletter_topic}} [/web_search]\n[web_search] site:{{premium_sources[1]}} {{newsletter_topic}} [/web_search]\n... (ripeti per tutte le fonti disponibili)\n\nSTEP 3: CONTENT ANALYSIS & STRUCTURING\nPer ogni contenuto estratto:\n- Estrai insights chiave e dati rilevanti\n- Identifica trend e pattern emergenti\n- Categorizza per sezione newsletter appropriata\n- Calcola relevance score per {{target_audience}}\n\nSTEP 4: INSIGHTS SYNTHESIS\nCrea contenuto strutturato per ogni sezione:\n1. Executive Summary insights\n2. Market Highlights data\n3. Premium Insights analysis\n4. Expert Analysis perspectives\n5. Actionable Recommendations\n6. Market Outlook predictions\n\nFILTERS:\n- Escludi topics in: {{exclude_topics}}\n- Prioritizza sezioni: {{priority_sections}}\n- Mantieni focus su: {{newsletter_topic}}\n\nOUTPUT:\nContenuti strutturati e analizzati pronti per la creazione della newsletter, organizzati per sezione con word count target e relevance scores.",
      "dependencies": ["task1_enhanced_context"]
    },
    {
      "id": "task3_newsletter_creation",
      "name": "Precision Newsletter Creation",
      "agent": "copywriter",
      "description_template": "TASK 3 - PRECISION NEWSLETTER CREATION:\n\nCONTEXT FROM PREVIOUS TASKS:\nBrief operativo: {{task1_enhanced_context_output}}\nContenuti premium analizzati: {{task2_premium_analysis_output}}\n\nOBJECTIVE:\nCrea la newsletter finale seguendo esattamente la struttura definita e rispettando i word count precisi per ogni sezione.\n\nNEWSLETTER SPECIFICATIONS:\n- Topic: {{newsletter_topic}}\n- Target Audience: {{target_audience}}\n- Edition: {{edition_number}}\n- Total Word Count: {{target_word_count}}\n- Custom Instructions: {{custom_instructions}}\n\nSTRUCTURA NEWSLETTER (7 SEZIONI):\n\n1. **EXECUTIVE SUMMARY** ({{target_word_count * 0.15}} words)\n   - Overview del tema principale\n   - Key takeaways della newsletter\n   - Hook per mantenere l'attenzione\n\n2. **MARKET HIGHLIGHTS** ({{target_word_count * 0.20}} words)\n   - Dati e statistiche chiave dalle fonti premium\n   - Trend di mercato rilevanti\n   - Performance indicators importanti\n\n3. **PREMIUM INSIGHTS** ({{target_word_count * 0.25}} words)\n   - Analisi approfondita dai contenuti premium\n   - Insights esclusivi e prospettive uniche\n   - Correlazioni e pattern identificati\n\n4. **EXPERT ANALYSIS** ({{target_word_count * 0.15}} words)\n   - Interpretazione professionale dei dati\n   - Implicazioni per {{target_audience}}\n   - Contesto storico e comparativo\n\n5. **ACTIONABLE RECOMMENDATIONS** ({{target_word_count * 0.15}} words)\n   - Azioni concrete per i lettori\n   - Strategie implementabili\n   - Timeline e priorità\n\n6. **MARKET OUTLOOK** ({{target_word_count * 0.07}} words)\n   - Previsioni a breve-medio termine\n   - Fattori da monitorare\n   - Scenari possibili\n\n7. **CLIENT-SPECIFIC CTA** ({{target_word_count * 0.03}} words)\n   - Call-to-action personalizzata per il cliente\n   - Link a servizi/prodotti rilevanti\n   - Contatti e next steps\n\nQUALITY REQUIREMENTS:\n- Rispetta esattamente il brand voice del cliente\n- Mantieni coerenza terminologica\n- Integra seamlessly i contenuti premium\n- Assicura flow narrativo coinvolgente\n- Verifica word count per ogni sezione\n- Include data e statistiche specifiche\n- Mantieni tone professionale ma accessibile\n\nOUTPUT:\nNewsletter completa in formato markdown con:\n- Struttura a 7 sezioni rispettando word count\n- Integrazione completa contenuti premium\n- Brand voice del cliente\n- Formattazione professionale\n- Metriche di qualità",
      "dependencies": ["task2_premium_analysis"]
    }
  ]
}
```

---

## 🎨 FRONTEND CONFIGURATION SPECIFICATIONS

### **📋 API Service Configuration**

**File**: `web/react-app/src/services/api.ts`

Add to `getWorkflowTypes()` array:

```typescript
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
      type: 'text', // Will be handled as array in form
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
```

### **📝 Form Schema and Validation**

**File**: `web/react-app/src/components/WorkflowForm.tsx`

Add after existing schemas (around line 82):

```typescript
// Premium Newsletter Schema
const premiumNewsletterSchema = yup.object({
  newsletter_topic: yup
    .string()
    .required('Newsletter topic is required')
    .min(5, 'Topic must be at least 5 characters')
    .max(200, 'Topic must be less than 200 characters'),
  premium_sources: yup
    .string()
    .required('At least one premium source is required')
    .test('valid-urls', 'Please enter valid URLs', function(value) {
      if (!value) return false;
      const urls = value.split('\n').filter(url => url.trim());
      if (urls.length === 0) return false;
      if (urls.length > 10) return this.createError({ message: 'Maximum 10 sources allowed' });

      for (const url of urls) {
        if (!url.trim().match(/^https?:\/\/.+/)) {
          return this.createError({ message: `Invalid URL: ${url.trim()}` });
        }
      }
      return true;
    }),
  target_audience: yup
    .string()
    .required('Target audience is required')
    .min(3, 'Target audience must be at least 3 characters')
    .max(500, 'Target audience must be less than 500 characters'),
  target_word_count: yup
    .number()
    .optional()
    .min(800, 'Minimum 800 words')
    .max(2500, 'Maximum 2500 words'),
  edition_number: yup
    .number()
    .optional()
    .min(1, 'Edition must be at least 1'),
  exclude_topics: yup
    .string()
    .optional(),
  priority_sections: yup
    .string()
    .optional(),
  custom_instructions: yup
    .string()
    .optional()
    .max(1000, 'Instructions must be less than 1000 characters')
});

// Type definition
type PremiumNewsletterFormData = {
  newsletter_topic: string;
  premium_sources: string;
  target_audience: string;
  target_word_count?: number;
  edition_number?: number;
  exclude_topics?: string;
  priority_sections?: string;
  custom_instructions?: string;
};
```

### **🎯 Form Logic Updates**

Add to `getValidationSchema()` function:

```typescript
if (selectedWorkflow?.id === 'premium_newsletter') {
  return premiumNewsletterSchema;
}
```

Add to `getDefaultValues()` function:

```typescript
if (selectedWorkflow?.id === 'premium_newsletter') {
  return {
    newsletter_topic: '',
    premium_sources: '',
    target_audience: selectedClient?.targetAudience || '',
    target_word_count: 1200,
    edition_number: 1,
    exclude_topics: '',
    priority_sections: '',
    custom_instructions: '',
  };
}
```

### **🎨 Form Rendering Function**

Add after existing render functions (around line 500):

```typescript
const renderPremiumNewsletterForm = () => (
  <Box>
    {/* Workflow Info Header */}
    <Paper sx={{ p: 2, mb: 3, backgroundColor: 'secondary.50' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
        <EmailIcon color="secondary" />
        <Typography variant="h6" color="secondary.main">
          Premium Newsletter
        </Typography>
      </Box>
      <Typography variant="body2" color="text.secondary">
        Advanced newsletter with premium source analysis and client-specific brand integration
      </Typography>
    </Paper>

    <Grid container spacing={3}>
      {/* Newsletter Topic */}
      <Grid item xs={12}>
        <Controller
          name="newsletter_topic"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Newsletter Topic *"
              placeholder="Enter the main theme for this newsletter edition"
              error={!!errors.newsletter_topic}
              helperText={errors.newsletter_topic?.message as string}
              multiline
              rows={2}
            />
          )}
        />
      </Grid>

      {/* Premium Sources URLs */}
      <Grid item xs={12}>
        <Controller
          name="premium_sources"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Premium Sources URLs *"
              placeholder="Enter premium source URLs (one per line, max 10)"
              error={!!errors.premium_sources}
              helperText={errors.premium_sources?.message as string || "Enter one URL per line. Maximum 10 sources allowed."}
              multiline
              rows={6}
            />
          )}
        />
      </Grid>

      {/* Target Audience */}
      <Grid item xs={12}>
        <Controller
          name="target_audience"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Target Audience *"
              placeholder="Describe the specific target audience for this edition"
              error={!!errors.target_audience}
              helperText={errors.target_audience?.message as string}
              multiline
              rows={3}
            />
          )}
        />
      </Grid>

      {/* Word Count & Edition Number */}
      <Grid item xs={12} sm={6}>
        <Controller
          name="target_word_count"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              type="number"
              label="Target Word Count"
              placeholder="1200"
              error={!!errors.target_word_count}
              helperText={errors.target_word_count?.message as string}
              InputProps={{ inputProps: { min: 800, max: 2500 } }}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} sm={6}>
        <Controller
          name="edition_number"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              type="number"
              label="Edition Number"
              placeholder="1"
              error={!!errors.edition_number}
              helperText={errors.edition_number?.message as string}
              InputProps={{ inputProps: { min: 1 } }}
            />
          )}
        />
      </Grid>

      {/* Exclude Topics */}
      <Grid item xs={12} sm={6}>
        <Controller
          name="exclude_topics"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Topics to Exclude"
              placeholder="Enter topics to exclude (comma-separated)"
              error={!!errors.exclude_topics}
              helperText={errors.exclude_topics?.message as string}
            />
          )}
        />
      </Grid>

      {/* Priority Sections */}
      <Grid item xs={12} sm={6}>
        <Controller
          name="priority_sections"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Priority Sections"
              placeholder="Enter priority sections (comma-separated)"
              error={!!errors.priority_sections}
              helperText={errors.priority_sections?.message as string}
            />
          )}
        />
      </Grid>

      {/* Custom Instructions */}
      <Grid item xs={12}>
        <Controller
          name="custom_instructions"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              fullWidth
              label="Custom Instructions"
              placeholder="Any additional instructions for the newsletter generation"
              error={!!errors.custom_instructions}
              helperText={errors.custom_instructions?.message as string}
              multiline
              rows={3}
            />
          )}
        />
      </Grid>
    </Grid>
  </Box>
);
```

Add conditional rendering in return statement:

```typescript
{selectedWorkflow.id === 'premium_newsletter' && renderPremiumNewsletterForm()}
```

---

## 🎯 IMPLEMENTATION PROMPT FOR AGENT

```markdown
# IMPLEMENTATION TASK: Premium Newsletter Workflow

## OBJECTIVE
Implement a new `premium_newsletter` workflow for the CGSRef system following the exact specifications and safety constraints provided in the PREMIUM_NEWSLETTER_IMPLEMENTATION_GUIDE.md file.

## CRITICAL CONSTRAINTS
1. **SAFETY FIRST**: Never modify existing enhanced_article workflow files
2. **ADDITIVE ONLY**: Only add new code, never modify existing functionality
3. **INCREMENTAL**: Implement in phases with validation after each step
4. **BACKWARD COMPATIBLE**: Enhanced_article workflow must continue working

## IMPLEMENTATION PHASES

### PHASE 1: Backend Foundation (REQUIRED)
Execute steps 1.1 through 1.5 from the implementation checklist:
- Create premium_newsletter_handler.py with complete handler class
- Create premium_newsletter.json template with 3-task structure
- Add imports to __init__.py files (additive only)
- Validate registration and backward compatibility

### PHASE 2: Frontend Integration (REQUIRED)
Execute steps 2.1 through 2.5 from the implementation checklist:
- Add workflow configuration to api.ts (additive only)
- Add form schema and validation to WorkflowForm.tsx
- Add form rendering logic and UI components
- Validate frontend integration and existing functionality

### PHASE 3: Advanced Components (OPTIONAL)
Only implement if specifically requested:
- Premium sources analyzer agent
- Premium financial sources tool
- Custom UI components for URL/tag arrays

### PHASE 4: Testing & Validation (REQUIRED)
Execute comprehensive testing as specified in checklist:
- Backend validation (server startup, workflow registry)
- Frontend validation (compilation, UI rendering)
- End-to-end validation (both workflows functional)

## SUCCESS CRITERIA
✅ Premium newsletter workflow appears in workflow selector
✅ Enhanced article workflow continues working unchanged
✅ New workflow form renders correctly with all fields
✅ System remains stable with no regressions
✅ All validation tests pass

## FAILURE CONDITIONS
❌ Enhanced article workflow stops working
❌ System becomes unstable or throws errors
❌ Existing functionality is modified or broken
❌ Import errors or dependency conflicts

## DELIVERABLES
1. All new files created as specified
2. Existing files modified only with additive changes
3. Comprehensive testing completed and passed
4. Documentation of any issues encountered
5. Confirmation that both workflows are functional

## REFERENCE DOCUMENTATION
Use the complete technical specifications provided in this file:
- Handler template with all required methods
- JSON template with 3-task structure
- Frontend configuration with form schema
- Validation requirements and safety guidelines

Follow the implementation checklist exactly and validate each step before proceeding.
```

---

## 📊 IMPLEMENTATION TIMELINE

| Phase | Duration | Dependencies | Risk Level |
|-------|----------|--------------|------------|
| **Phase 1: Backend** | 2 hours | None | 🟡 Medium |
| **Phase 2: Frontend** | 1.5 hours | Phase 1 complete | 🟡 Medium |
| **Phase 3: Advanced** | 3 hours | Phase 2 complete | 🟠 High |
| **Phase 4: Testing** | 1 hour | All phases | 🟢 Low |
| **Total** | 7.5 hours | Sequential | 🟡 Medium |

---

## ✅ FINAL CHECKLIST

### **Pre-Implementation** ☑️
- [ ] Current system is stable and enhanced_article works
- [ ] Git repository is clean with recent commit
- [ ] Development environment is ready
- [ ] Implementation guide is understood

### **Post-Implementation** ☑️
- [ ] Premium newsletter workflow is available in UI
- [ ] Enhanced article workflow still works perfectly
- [ ] No errors in backend or frontend logs
- [ ] All validation tests pass
- [ ] System performance is unchanged
- [ ] Documentation is updated

### **Success Verification** ☑️
- [ ] Both workflows appear in workflow selector
- [ ] Both workflows can be selected and used
- [ ] Forms render correctly for both workflows
- [ ] No regressions in existing functionality
- [ ] System is ready for production use

---

**Implementation Guide Status**: ✅ READY FOR EXECUTION
**Safety Level**: 🛡️ PRODUCTION-SAFE
**Estimated Success Rate**: 95%+ with careful execution
**Total File Size**: Complete implementation guide with all specifications
```
