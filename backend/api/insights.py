"""
Insights API routes — summarization, extraction, risk detection.
"""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models.document import Document, DocumentStatus
from backend.models.insight import DocumentInsight, InsightType
from backend.models.schemas import (
    ExtractionRequest,
    ExtractionResponse,
    RiskResponse,
    SummaryResponse,
)
from backend.services.rag_service import detect_risks, extract_key_info, generate_summary
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/documents", tags=["Insights"])


async def _get_ready_document(document_id: int, db: AsyncSession) -> Document:
    """Helper: fetch a document and verify it's ready."""
    result = await db.execute(select(Document).filter(Document.id == document_id))
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.status != DocumentStatus.READY:
        raise HTTPException(status_code=400, detail=f"Document not ready. Status: {doc.status}")
    
    return doc


@router.post("/{document_id}/summarize", response_model=SummaryResponse)
async def summarize_document(document_id: int, db: AsyncSession = Depends(get_db)):
    """Generate AI-powered summary for a document."""
    doc = await _get_ready_document(document_id, db)
    
    logger.info("summarize_request", doc_id=document_id)
    
    # Generate summary
    summary = generate_summary(doc.text_content, document_id)
    
    # Save insight
    insight = DocumentInsight(
        document_id=document_id,
        insight_type=InsightType.SUMMARY,
        content_json=json.dumps(summary),
    )
    db.add(insight)
    await db.commit()
    
    return SummaryResponse(
        document_id=document_id,
        executive_summary=summary.get("executive_summary", ""),
        section_summaries=summary.get("section_summaries", []),
        bullet_highlights=summary.get("bullet_highlights", []),
        key_takeaways=summary.get("key_takeaways", []),
    )


@router.post("/{document_id}/extract", response_model=ExtractionResponse)
async def extract_document(
    document_id: int,
    request: ExtractionRequest = ExtractionRequest(),
    db: AsyncSession = Depends(get_db),
):
    """Extract key information based on document type."""
    doc = await _get_ready_document(document_id, db)
    
    logger.info("extract_request", doc_id=document_id, doc_type=request.document_type)
    
    extraction = extract_key_info(doc.text_content, document_id, request.document_type.value)
    
    # Save insight
    insight = DocumentInsight(
        document_id=document_id,
        insight_type=InsightType.EXTRACTION,
        content_json=json.dumps(extraction),
    )
    db.add(insight)
    await db.commit()
    
    return ExtractionResponse(
        document_id=document_id,
        document_type=request.document_type.value,
        extracted_data=extraction,
    )


@router.post("/{document_id}/risks", response_model=RiskResponse)
async def detect_document_risks(document_id: int, db: AsyncSession = Depends(get_db)):
    """Detect risks and compliance issues in a document."""
    doc = await _get_ready_document(document_id, db)
    
    logger.info("risk_detection_request", doc_id=document_id)
    
    risk_report = detect_risks(doc.text_content, document_id)
    
    # Save insight
    insight = DocumentInsight(
        document_id=document_id,
        insight_type=InsightType.RISK,
        content_json=json.dumps(risk_report),
    )
    db.add(insight)
    await db.commit()
    
    return RiskResponse(
        document_id=document_id,
        overall_risk_score=risk_report.get("overall_risk_score", "Medium"),
        risk_items=risk_report.get("risk_items", []),
        total_risks=len(risk_report.get("risk_items", [])),
    )


@router.get("/{document_id}/insights")
async def get_document_insights(document_id: int, db: AsyncSession = Depends(get_db)):
    """Get all generated insights for a document."""
    # Verify document exists
    result = await db.execute(select(Document).filter(Document.id == document_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Fetch insights
    result = await db.execute(
        select(DocumentInsight)
        .filter(DocumentInsight.document_id == document_id)
        .order_by(DocumentInsight.created_at.desc())
    )
    insights = result.scalars().all()
    
    formatted = []
    for insight in insights:
        try:
            content = json.loads(insight.content_json)
        except json.JSONDecodeError:
            content = {"raw": insight.content_json}
        
        formatted.append({
            "id": insight.id,
            "type": insight.insight_type.value,
            "content": content,
            "created_at": insight.created_at.isoformat(),
        })
    
    return {
        "document_id": document_id,
        "insights": formatted,
        "total": len(formatted),
    }
