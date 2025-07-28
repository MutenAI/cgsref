"""Knowledge base endpoints for RAG content management."""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from pathlib import Path
import os
from datetime import datetime

from core.infrastructure.tools.rag_tool import RAGTool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge-base", tags=["knowledge-base"])


class DocumentInfo(BaseModel):
    """Document information model."""
    id: str
    title: str
    filename: str
    description: str
    content_preview: str
    tags: List[str]
    last_modified: str
    size_bytes: int
    content_type: str = "markdown"


class ClientDocumentsResponse(BaseModel):
    """Response model for client documents."""
    client_name: str
    total_documents: int
    documents: List[DocumentInfo]


class DocumentContentResponse(BaseModel):
    """Response model for document content."""
    document_id: str
    title: str
    content: str
    metadata: Dict[str, Any]


def get_rag_tool() -> RAGTool:
    """Get RAG tool instance."""
    return RAGTool()


@router.get("/clients/{client_name}/documents", response_model=ClientDocumentsResponse)
async def get_client_documents(
    client_name: str,
    search: Optional[str] = Query(None, description="Search query to filter documents"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    rag_tool: RAGTool = Depends(get_rag_tool)
) -> ClientDocumentsResponse:
    """
    Get all documents for a specific client.
    
    Args:
        client_name: Name of the client
        search: Optional search query
        tags: Optional list of tags to filter by
        rag_tool: RAG tool instance
        
    Returns:
        List of documents with metadata
    """
    logger.info(f"📚 Getting documents for client: {client_name}")
    
    try:
        # Get client directory
        client_dir = rag_tool.rag_base_dir / client_name
        
        if not client_dir.exists():
            logger.warning(f"Knowledge base not found for client: {client_name}")
            return ClientDocumentsResponse(
                client_name=client_name,
                total_documents=0,
                documents=[]
            )
        
        documents = []
        
        # Process all markdown files
        for doc_path in client_dir.glob("*.md"):
            try:
                # Read file content
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract metadata from content
                doc_info = _extract_document_metadata(doc_path, content)
                
                # Apply filters
                if search and search.lower() not in doc_info.title.lower() and search.lower() not in content.lower():
                    continue
                
                if tags and not any(tag in doc_info.tags for tag in tags):
                    continue
                
                documents.append(doc_info)
                
            except Exception as e:
                logger.error(f"Error processing document {doc_path}: {str(e)}")
                continue
        
        # Sort by last modified (newest first)
        documents.sort(key=lambda x: x.last_modified, reverse=True)
        
        logger.info(f"✅ Found {len(documents)} documents for {client_name}")
        
        return ClientDocumentsResponse(
            client_name=client_name,
            total_documents=len(documents),
            documents=documents
        )
        
    except Exception as e:
        logger.error(f"Error getting documents for {client_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


@router.get("/clients/{client_name}/documents/{document_id}", response_model=DocumentContentResponse)
async def get_document_content(
    client_name: str,
    document_id: str,
    rag_tool: RAGTool = Depends(get_rag_tool)
) -> DocumentContentResponse:
    """
    Get full content of a specific document.
    
    Args:
        client_name: Name of the client
        document_id: ID of the document (filename without extension)
        rag_tool: RAG tool instance
        
    Returns:
        Document content with metadata
    """
    logger.info(f"📄 Getting document content: {client_name}/{document_id}")
    
    try:
        # Get document content using RAG tool
        content = await rag_tool.get_client_content(client_name, document_id)
        
        if content.startswith("Document") and "not found" in content:
            raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        # Get document file for metadata
        client_dir = rag_tool.rag_base_dir / client_name
        doc_path = client_dir / f"{document_id}.md"
        
        if not doc_path.exists():
            # Try without .md extension
            doc_path = client_dir / document_id
            if not doc_path.exists():
                raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
        
        # Extract metadata
        doc_info = _extract_document_metadata(doc_path, content)
        
        return DocumentContentResponse(
            document_id=document_id,
            title=doc_info.title,
            content=content,
            metadata={
                "filename": doc_info.filename,
                "tags": doc_info.tags,
                "last_modified": doc_info.last_modified,
                "size_bytes": doc_info.size_bytes,
                "content_type": doc_info.content_type
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting document content {client_name}/{document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving document: {str(e)}")


@router.get("/clients", response_model=List[str])
async def get_available_clients(
    rag_tool: RAGTool = Depends(get_rag_tool)
) -> List[str]:
    """
    Get list of available clients with knowledge bases.

    Returns:
        List of client names
    """
    logger.info("📋 Getting available clients")

    try:
        clients = []

        # Scan knowledge base directory
        if rag_tool.rag_base_dir.exists():
            for client_dir in rag_tool.rag_base_dir.iterdir():
                if client_dir.is_dir() and any(client_dir.glob("*.md")):
                    clients.append(client_dir.name)

        clients.sort()
        logger.info(f"✅ Found {len(clients)} clients: {clients}")

        return clients

    except Exception as e:
        logger.error(f"Error getting available clients: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving clients: {str(e)}")


class FrontendDocument(BaseModel):
    """Frontend-compatible document model."""
    id: str
    title: str
    description: str
    date: str
    category: str
    tags: List[str]
    selected: bool = False


@router.get("/frontend/clients/{client_name}/documents", response_model=List[FrontendDocument])
async def get_frontend_documents(
    client_name: str,
    search: Optional[str] = Query(None, description="Search query to filter documents"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    rag_tool: RAGTool = Depends(get_rag_tool)
) -> List[FrontendDocument]:
    """
    Get documents in frontend-compatible format.

    Args:
        client_name: Name of the client
        search: Optional search query
        tags: Optional list of tags to filter by
        rag_tool: RAG tool instance

    Returns:
        List of documents in frontend format
    """
    logger.info(f"🎨 Getting frontend documents for client: {client_name}")

    try:
        # Get documents using existing endpoint logic
        client_dir = rag_tool.rag_base_dir / client_name

        if not client_dir.exists():
            logger.warning(f"Knowledge base not found for client: {client_name}")
            return []

        documents = []

        # Process all markdown files
        for doc_path in client_dir.glob("*.md"):
            try:
                # Read file content
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract metadata from content
                doc_info = _extract_document_metadata(doc_path, content)

                # Apply filters
                if search and search.lower() not in doc_info.title.lower() and search.lower() not in content.lower():
                    continue

                if tags and not any(tag in doc_info.tags for tag in tags):
                    continue

                # Convert to frontend format
                frontend_doc = FrontendDocument(
                    id=doc_info.id,
                    title=doc_info.title,
                    description=doc_info.description,
                    date=doc_info.last_modified[:10],  # YYYY-MM-DD format
                    category=doc_info.tags[0] if doc_info.tags else "general",
                    tags=doc_info.tags,
                    selected=False
                )

                documents.append(frontend_doc)

            except Exception as e:
                logger.error(f"Error processing document {doc_path}: {str(e)}")
                continue

        # Sort by last modified (newest first)
        documents.sort(key=lambda x: x.date, reverse=True)

        logger.info(f"✅ Returning {len(documents)} frontend documents for {client_name}")

        return documents

    except Exception as e:
        logger.error(f"Error getting frontend documents for {client_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


def _extract_document_metadata(doc_path: Path, content: str) -> DocumentInfo:
    """Extract metadata from document."""
    filename = doc_path.name
    doc_id = doc_path.stem
    
    # Extract title from first heading or filename
    title = filename.replace('.md', '').replace('_', ' ').title()
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Extract description from first paragraph
    description = ""
    in_content = False
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            in_content = True
            continue
        if in_content and line and not line.startswith('#'):
            description = line[:200] + "..." if len(line) > 200 else line
            break
    
    # Extract tags from filename and content
    tags = []
    
    # Tags from filename
    if 'company' in filename.lower() or 'profile' in filename.lower():
        tags.extend(['company', 'profile'])
    if 'guideline' in filename.lower() or 'guide' in filename.lower():
        tags.extend(['guidelines', 'style'])
    if 'content' in filename.lower():
        tags.append('content')
    if 'financial' in filename.lower() or 'finance' in filename.lower():
        tags.append('finance')
    if 'market' in filename.lower():
        tags.append('markets')
    if 'gen-z' in filename.lower() or 'genz' in filename.lower():
        tags.append('gen-z')
    if 'invest' in filename.lower():
        tags.append('investing')
    
    # Tags from content
    content_lower = content.lower()
    if 'gen z' in content_lower or 'generation z' in content_lower:
        tags.append('gen-z')
    if 'invest' in content_lower:
        tags.append('investing')
    if 'financ' in content_lower:
        tags.append('finance')
    if 'market' in content_lower:
        tags.append('markets')
    if '2024' in content or '2025' in content:
        tags.append('2024')
    
    # Remove duplicates
    tags = list(set(tags))
    
    # Get file stats
    stat = doc_path.stat()
    last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
    size_bytes = stat.st_size
    
    # Create preview (first 300 chars of content, excluding title)
    content_lines = [line for line in lines if line.strip() and not line.startswith('#')]
    preview_text = ' '.join(content_lines)[:300]
    if len(preview_text) == 300:
        preview_text += "..."
    
    return DocumentInfo(
        id=doc_id,
        title=title,
        filename=filename,
        description=description or preview_text,
        content_preview=preview_text,
        tags=tags,
        last_modified=last_modified,
        size_bytes=size_bytes,
        content_type="markdown"
    )
