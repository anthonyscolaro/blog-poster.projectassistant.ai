"""
Enhanced Legal Fact Checker Agent with Real-Time Verification
Verifies ADA compliance claims and legal accuracy using official sources and web scraping
"""
import os
import re
import json
import logging
import hashlib
import aiohttp
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
from urllib.parse import quote

from pydantic import BaseModel, Field
import asyncio
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class LegalClaimType(str, Enum):
    """Types of legal claims to verify"""
    ADA_REQUIREMENT = "ada_requirement"
    SERVICE_ANIMAL_RULE = "service_animal_rule"
    BUSINESS_OBLIGATION = "business_obligation"
    HANDLER_RIGHT = "handler_right"
    LEGAL_CITATION = "legal_citation"
    REGISTRATION_CLAIM = "registration_claim"
    ACCESS_RIGHT = "access_right"
    EXCLUSION_RULE = "exclusion_rule"
    STATE_LAW = "state_law"
    FEDERAL_LAW = "federal_law"
    DOJ_GUIDANCE = "doj_guidance"
    CASE_LAW = "case_law"


class VerificationStatus(str, Enum):
    """Verification status for claims"""
    VERIFIED = "verified"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    NEEDS_CLARIFICATION = "needs_clarification"
    UNVERIFIABLE = "unverifiable"
    OUTDATED = "outdated"
    CONTEXT_DEPENDENT = "context_dependent"


class ComplianceViolation(BaseModel):
    """Represents a compliance violation in content"""
    type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    location: Optional[str] = None
    regulation_reference: Optional[str] = None
    suggested_fix: Optional[str] = None


class LegalClaim(BaseModel):
    """Individual legal claim to verify"""
    text: str
    claim_type: LegalClaimType
    context: Optional[str] = None
    source_paragraph: Optional[str] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    entities: List[str] = Field(default_factory=list)  # Named entities in claim


class VerificationResult(BaseModel):
    """Result of verifying a legal claim"""
    claim: LegalClaim
    status: VerificationStatus
    correct_statement: Optional[str] = None
    legal_citations: List[str] = Field(default_factory=list)
    official_sources: List[str] = Field(default_factory=list)
    explanation: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    verification_method: str = "static"  # "static", "web", "ai", "hybrid"
    verified_at: datetime = Field(default_factory=datetime.now)


class LegalFactCheckReport(BaseModel):
    """Complete fact-checking report for an article"""
    article_title: str
    total_claims: int
    verified_claims: int
    incorrect_claims: int
    partially_correct_claims: int
    verification_results: List[VerificationResult]
    compliance_violations: List[ComplianceViolation] = Field(default_factory=list)
    required_disclaimers: List[str]
    suggested_corrections: List[Dict[str, str]]
    overall_accuracy_score: float = Field(ge=0.0, le=1.0)
    compliance_score: float = Field(ge=0.0, le=1.0)
    checked_at: datetime = Field(default_factory=datetime.now)
    report_summary: str = ""


class EnhancedLegalFactCheckerAgent:
    """
    Enhanced agent for comprehensive legal fact-checking with real-time verification
    """
    
    # Comprehensive ADA facts database
    ADA_FACTS_DATABASE = {
        "core_definitions": {
            "service_animal_definition": {
                "fact": "Service animals are defined as dogs that are individually trained to do work or perform tasks for people with disabilities. The work or task must be directly related to the person's disability.",
                "citation": "28 CFR §36.302(c)(1)",
                "source": "https://www.ada.gov/resources/service-animals-2010-requirements/",
                "last_verified": "2024-01-01",
                "exceptions": ["Miniature horses may be permitted under specific conditions per 28 CFR §36.302(c)(9)"]
            },
            "disability_definition": {
                "fact": "A disability is a physical or mental impairment that substantially limits one or more major life activities.",
                "citation": "42 U.S.C. §12102",
                "source": "https://www.ada.gov/law-and-regs/ada/",
                "last_verified": "2024-01-01"
            }
        },
        "business_requirements": {
            "two_questions": {
                "fact": "Staff may ask only two questions: (1) is the dog a service animal required because of a disability, and (2) what work or task has the dog been trained to perform.",
                "citation": "28 CFR §36.302(c)(6)",
                "source": "https://www.ada.gov/resources/service-animals-faqs/",
                "prohibited": ["Cannot ask about the person's disability", "Cannot request documentation", "Cannot require special identification", "Cannot ask for demonstration of task"]
            },
            "no_extra_charges": {
                "fact": "People with disabilities who use service animals cannot be charged extra fees, deposits, or surcharges, even if pets are subject to such fees.",
                "citation": "28 CFR §36.302(c)(8)",
                "source": "https://www.ada.gov/resources/service-animals-faqs/",
                "clarification": "Damage caused by service animal can be charged if normally charged for damage by customers"
            },
            "access_rights": {
                "fact": "Service animals must be allowed in all areas where customers are normally allowed to go, including restaurants, stores, hotels, and public transportation.",
                "citation": "28 CFR §36.302(c)(7)",
                "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302",
                "exceptions": ["Sterile environments", "Where animal poses direct threat", "Religious entities exempt under Title III"]
            }
        },
        "handler_responsibilities": {
            "care_and_control": {
                "fact": "The handler is responsible for caring for and supervising the service animal, including toileting, feeding, grooming and veterinary care. Staff are not required to provide these services.",
                "citation": "28 CFR §36.302(c)(5)",
                "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302"
            },
            "control_requirements": {
                "fact": "Service animals must be under control of the handler, typically via harness, leash, or tether unless these devices interfere with the animal's work or the individual's disability prevents their use.",
                "citation": "28 CFR §36.302(c)(4)",
                "source": "https://www.ada.gov/resources/service-animals-2010-requirements/"
            }
        },
        "removal_conditions": {
            "legitimate_removal": {
                "fact": "A service animal may be removed if: (1) The animal is out of control and the handler does not take effective action to control it, or (2) The animal is not housebroken.",
                "citation": "28 CFR §36.302(c)(2)",
                "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302",
                "important_note": "Even if animal is removed, business must offer to provide services without the animal present"
            }
        },
        "common_misconceptions": {
            "no_registration": {
                "fact": "The ADA does not require service animals to be registered, certified, licensed, or have special identification. There is no official federal registry.",
                "citation": "28 CFR §36.302(c)",
                "source": "https://www.ada.gov/resources/service-animals-2010-requirements/",
                "warning": "Many online 'registries' are scams that have no legal value"
            },
            "no_breed_restrictions": {
                "fact": "The ADA does not restrict the breeds of dogs that can be service animals. Local breed bans do not apply to service animals.",
                "citation": "28 CFR §36.302(c)",
                "source": "https://www.ada.gov/resources/service-animals-faqs/",
                "clarification": "However, the animal must not pose a direct threat based on its behavior"
            },
            "emotional_support_difference": {
                "fact": "Emotional support animals, comfort animals, and therapy dogs are not service animals under Title II and Title III of the ADA because they are not trained to perform specific tasks.",
                "citation": "28 CFR §36.302(c)(1)",
                "source": "https://www.ada.gov/resources/service-animals-faqs/",
                "note": "ESAs may have rights under Fair Housing Act or Air Carrier Access Act"
            }
        }
    }
    
    # Expanded misconception detection patterns
    MISCONCEPTION_PATTERNS = {
        "registration_myths": [
            r"must\s+be\s+registered",
            r"require[sd]?\s+registration",
            r"official\s+registry",
            r"certification\s+required",
            r"need[s]?\s+certification",
            r"must\s+have\s+papers"
        ],
        "identification_myths": [
            r"must\s+wear\s+(?:a\s+)?vest",
            r"require[sd]?\s+identification",
            r"special\s+ID",
            r"service\s+dog\s+card",
            r"must\s+display"
        ],
        "documentation_myths": [
            r"can\s+ask\s+for\s+(?:proof|documentation)",
            r"require[sd]?\s+doctor'?s?\s+note",
            r"medical\s+documentation",
            r"proof\s+of\s+disability"
        ],
        "training_myths": [
            r"must\s+be\s+professionally\s+trained",
            r"require[sd]?\s+professional\s+training",
            r"certified\s+trainer",
            r"training\s+certification"
        ],
        "esa_confusion": [
            r"emotional\s+support\s+(?:animals?|dogs?)\s+(?:are|have)\s+(?:the\s+)?same",
            r"ESA[s]?\s+(?:are|have)\s+(?:the\s+)?same\s+rights",
            r"comfort\s+animals?\s+are\s+service"
        ]
    }
    
    def __init__(
        self,
        research_dir: str = "research/legal/ada-official",
        jina_api_key: Optional[str] = None,
        cache_dir: str = "cache/legal_verification",
        enable_web_verification: bool = True
    ):
        """
        Initialize the enhanced legal fact checker agent
        
        Args:
            research_dir: Directory containing ADA research documents
            jina_api_key: API key for Jina AI web scraping
            cache_dir: Directory for caching verification results
            enable_web_verification: Whether to enable real-time web verification
        """
        self.research_dir = Path(research_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.jina_api_key = jina_api_key or os.getenv("JINA_API_KEY")
        self.enable_web_verification = enable_web_verification and self.jina_api_key
        
        self.legal_sources = self._load_legal_sources()
        self.verification_cache = {}
        self.session = None
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = self._compile_patterns()
        
        # Legal citation patterns
        self.citation_patterns = [
            re.compile(r'\b\d+\s+CFR\s+§?\s*\d+(?:\.\d+)*\b'),  # Federal regulations
            re.compile(r'\b28\s+CFR\s+(?:Part\s+)?\d+\b'),       # Title 28 CFR
            re.compile(r'\bADA\s+Title\s+[IVX]+\b'),             # ADA Titles
            re.compile(r'\b42\s+U\.?S\.?C\.?\s+§?\s*\d+\b'),    # US Code
            re.compile(r'\bPub\.?\s*L\.?\s+\d+-\d+\b'),          # Public Laws
        ]
    
    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile regex patterns for efficiency"""
        compiled = {}
        for category, patterns in self.MISCONCEPTION_PATTERNS.items():
            compiled[category] = [re.compile(p, re.IGNORECASE) for p in patterns]
        return compiled
    
    def _load_legal_sources(self) -> Dict[str, str]:
        """Load ADA research documents from disk"""
        sources = {}
        
        if not self.research_dir.exists():
            self.research_dir.mkdir(parents=True, exist_ok=True)
            logger.warning(f"Created research directory: {self.research_dir}")
        
        # Load all markdown and text files from research directory
        for file_path in self.research_dir.rglob("*"):
            if file_path.suffix in ['.md', '.txt', '.json']:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        rel_path = file_path.relative_to(self.research_dir)
                        sources[str(rel_path)] = content
                        logger.info(f"Loaded legal source: {rel_path}")
                except Exception as e:
                    logger.error(f"Failed to load {file_path}: {e}")
        
        logger.info(f"Loaded {len(sources)} legal source documents")
        return sources
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fact_check_article(
        self,
        article_content: str,
        article_title: str = "Untitled Article",
        check_citations: bool = True,
        check_claims: bool = True,
        suggest_corrections: bool = True,
        verify_online: bool = True
    ) -> LegalFactCheckReport:
        """
        Perform comprehensive fact-checking on an article with enhanced verification
        
        Args:
            article_content: The article text to check
            article_title: Title of the article
            check_citations: Whether to verify legal citations
            check_claims: Whether to verify factual claims
            suggest_corrections: Whether to suggest corrections
            verify_online: Whether to perform real-time web verification
        
        Returns:
            LegalFactCheckReport with comprehensive verification results
        """
        logger.info(f"Starting fact-check for article: {article_title}")
        
        # Extract and categorize claims
        claims = await self._extract_and_categorize_claims(article_content)
        logger.info(f"Extracted {len(claims)} claims from article")
        
        # Verify each claim with enhanced methods
        verification_results = []
        for i, claim in enumerate(claims):
            logger.debug(f"Verifying claim {i+1}/{len(claims)}: {claim.text[:50]}...")
            
            if verify_online and self.enable_web_verification:
                result = await self._verify_claim_enhanced(claim)
            else:
                result = await self._verify_claim_static(claim)
            
            verification_results.append(result)
        
        # Check for compliance violations
        compliance_violations = self._check_compliance_violations(article_content, verification_results)
        
        # Check for required disclaimers
        disclaimers = self._check_comprehensive_disclaimers(article_content)
        
        # Generate corrections if requested
        corrections = []
        if suggest_corrections:
            corrections = self._generate_smart_corrections(verification_results)
        
        # Calculate scores
        verified = sum(1 for r in verification_results if r.status == VerificationStatus.VERIFIED)
        incorrect = sum(1 for r in verification_results if r.status == VerificationStatus.INCORRECT)
        partial = sum(1 for r in verification_results if r.status == VerificationStatus.PARTIALLY_CORRECT)
        
        total = len(verification_results)
        accuracy_score = (verified + (partial * 0.5)) / max(1, total)
        
        # Calculate compliance score
        critical_violations = sum(1 for v in compliance_violations if v.severity == "critical")
        high_violations = sum(1 for v in compliance_violations if v.severity == "high")
        compliance_score = max(0, 1 - (critical_violations * 0.3 + high_violations * 0.15))
        
        # Generate report summary
        summary = self._generate_report_summary(
            accuracy_score, compliance_score, verified, incorrect, partial, total
        )
        
        return LegalFactCheckReport(
            article_title=article_title,
            total_claims=total,
            verified_claims=verified,
            incorrect_claims=incorrect,
            partially_correct_claims=partial,
            verification_results=verification_results,
            compliance_violations=compliance_violations,
            required_disclaimers=disclaimers,
            suggested_corrections=corrections,
            overall_accuracy_score=accuracy_score,
            compliance_score=compliance_score,
            report_summary=summary
        )
    
    async def _extract_and_categorize_claims(self, content: str) -> List[LegalClaim]:
        """Extract and categorize legal claims using NLP techniques"""
        claims = []
        
        # Split into paragraphs for context
        paragraphs = content.split('\n\n')
        
        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue
            
            # Split into sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            for sent_idx, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Analyze sentence for legal claims
                claim_indicators = self._analyze_sentence_for_claims(sentence)
                
                if claim_indicators['is_claim']:
                    # Extract named entities
                    entities = self._extract_entities(sentence)
                    
                    # Get context (previous and next sentence if available)
                    context_sentences = []
                    if sent_idx > 0:
                        context_sentences.append(sentences[sent_idx - 1])
                    if sent_idx < len(sentences) - 1:
                        context_sentences.append(sentences[sent_idx + 1])
                    
                    claims.append(LegalClaim(
                        text=sentence,
                        claim_type=claim_indicators['claim_type'],
                        context=' '.join(context_sentences) if context_sentences else None,
                        source_paragraph=paragraph,
                        confidence=claim_indicators['confidence'],
                        entities=entities
                    ))
        
        # Also extract citations as claims
        citations = self._extract_citations(content)
        for citation in citations:
            claims.append(LegalClaim(
                text=f"Citation: {citation}",
                claim_type=LegalClaimType.LEGAL_CITATION,
                confidence=0.9
            ))
        
        return claims
    
    def _analyze_sentence_for_claims(self, sentence: str) -> Dict[str, Any]:
        """Analyze a sentence to determine if it contains a legal claim"""
        sentence_lower = sentence.lower()
        indicators = {
            'is_claim': False,
            'claim_type': LegalClaimType.ADA_REQUIREMENT,
            'confidence': 0.0
        }
        
        # Keywords that indicate legal claims
        legal_keywords = {
            'must': 0.9, 'shall': 0.9, 'required': 0.9, 'prohibited': 0.9,
            'cannot': 0.85, 'may not': 0.85, 'illegal': 0.9, 'unlawful': 0.9,
            'allowed': 0.8, 'permitted': 0.8, 'rights': 0.8, 'obligation': 0.85,
            'ada requires': 0.95, 'under the ada': 0.9, 'federal law': 0.85,
            'violat': 0.8, 'comply': 0.8, 'enforce': 0.8, 'entitle': 0.8
        }
        
        # Check for legal keywords
        max_confidence = 0.0
        for keyword, confidence in legal_keywords.items():
            if keyword in sentence_lower:
                max_confidence = max(max_confidence, confidence)
        
        if max_confidence > 0.5:
            indicators['is_claim'] = True
            indicators['confidence'] = max_confidence
            
            # Determine claim type
            indicators['claim_type'] = self._determine_detailed_claim_type(sentence)
        
        return indicators
    
    def _determine_detailed_claim_type(self, sentence: str) -> LegalClaimType:
        """Determine the specific type of legal claim with enhanced categorization"""
        sentence_lower = sentence.lower()
        
        # Check for specific claim types
        if any(pattern in sentence_lower for pattern in ['28 cfr', '42 u.s.c', 'section', '§']):
            return LegalClaimType.LEGAL_CITATION
        
        if 'state law' in sentence_lower or 'local' in sentence_lower:
            return LegalClaimType.STATE_LAW
        
        if 'doj' in sentence_lower or 'department of justice' in sentence_lower:
            return LegalClaimType.DOJ_GUIDANCE
        
        if 'case' in sentence_lower or 'court' in sentence_lower or 'ruling' in sentence_lower:
            return LegalClaimType.CASE_LAW
        
        if any(term in sentence_lower for term in ['service animal', 'service dog']):
            if any(term in sentence_lower for term in ['definition', 'defined', 'means']):
                return LegalClaimType.SERVICE_ANIMAL_RULE
            elif any(term in sentence_lower for term in ['registration', 'certification', 'identification']):
                return LegalClaimType.REGISTRATION_CLAIM
        
        if any(term in sentence_lower for term in ['business', 'establishment', 'facility', 'employer']):
            return LegalClaimType.BUSINESS_OBLIGATION
        
        if any(term in sentence_lower for term in ['handler', 'owner', 'person with disability']):
            return LegalClaimType.HANDLER_RIGHT
        
        if any(term in sentence_lower for term in ['access', 'admission', 'enter', 'allowed']):
            return LegalClaimType.ACCESS_RIGHT
        
        if any(term in sentence_lower for term in ['remove', 'exclude', 'deny', 'refuse']):
            return LegalClaimType.EXCLUSION_RULE
        
        return LegalClaimType.ADA_REQUIREMENT
    
    def _extract_entities(self, sentence: str) -> List[str]:
        """Extract named entities from a sentence"""
        entities = []
        
        # Simple entity extraction (could be enhanced with NLP libraries)
        entity_patterns = [
            r'\bADA\b',
            r'\bDOJ\b',
            r'\bTitle [IVX]+\b',
            r'\bAmericans with Disabilities Act\b',
            r'\bDepartment of Justice\b',
            r'\bFair Housing Act\b',
            r'\bAir Carrier Access Act\b'
        ]
        
        for pattern in entity_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            entities.extend(matches)
        
        return list(set(entities))
    
    def _extract_citations(self, content: str) -> List[str]:
        """Extract legal citations from content"""
        citations = []
        
        for pattern in self.citation_patterns:
            matches = pattern.findall(content)
            citations.extend(matches)
        
        return list(set(citations))
    
    async def _verify_claim_enhanced(self, claim: LegalClaim) -> VerificationResult:
        """Verify a claim using enhanced methods including web verification"""
        # Try cache first
        claim_hash = hashlib.md5(claim.text.encode()).hexdigest()
        cache_file = self.cache_dir / f"{claim_hash}.json"
        
        if cache_file.exists():
            # Check if cache is fresh (within 7 days)
            if datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime) < timedelta(days=7):
                try:
                    with open(cache_file, 'r') as f:
                        cached_result = json.load(f)
                        return VerificationResult(**cached_result)
                except Exception as e:
                    logger.warning(f"Failed to load cached result: {e}")
        
        # Perform verification
        result = await self._verify_claim_static(claim)
        
        # If not definitively verified, try web verification
        if result.status in [VerificationStatus.NEEDS_CLARIFICATION, VerificationStatus.UNVERIFIABLE]:
            if self.enable_web_verification:
                web_result = await self._verify_claim_web(claim)
                if web_result.confidence_score > result.confidence_score:
                    result = web_result
        
        # Cache the result
        try:
            with open(cache_file, 'w') as f:
                json.dump(result.dict(), f, default=str)
        except Exception as e:
            logger.warning(f"Failed to cache result: {e}")
        
        return result
    
    async def _verify_claim_static(self, claim: LegalClaim) -> VerificationResult:
        """Verify a claim against static ADA facts database"""
        claim_lower = claim.text.lower()
        
        # Check against comprehensive facts database
        for category, facts in self.ADA_FACTS_DATABASE.items():
            for fact_key, fact_data in facts.items():
                if self._check_claim_against_fact(claim_lower, fact_data):
                    # Check if it's a contradiction or alignment
                    is_contradiction = self._is_contradiction(claim_lower, fact_data)
                    
                    if is_contradiction:
                        return VerificationResult(
                            claim=claim,
                            status=VerificationStatus.INCORRECT,
                            correct_statement=fact_data["fact"],
                            legal_citations=[fact_data["citation"]],
                            official_sources=[fact_data["source"]],
                            explanation=f"This claim contradicts official ADA guidance. {fact_data['fact']}",
                            confidence_score=0.9,
                            verification_method="static"
                        )
                    else:
                        return VerificationResult(
                            claim=claim,
                            status=VerificationStatus.VERIFIED,
                            correct_statement=None,
                            legal_citations=[fact_data["citation"]],
                            official_sources=[fact_data["source"]],
                            explanation="This claim aligns with official ADA requirements.",
                            confidence_score=0.85,
                            verification_method="static"
                        )
        
        # Check against misconception patterns
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(claim.text):
                    correct_fact = self._get_correct_fact_for_misconception_category(category)
                    return VerificationResult(
                        claim=claim,
                        status=VerificationStatus.INCORRECT,
                        correct_statement=correct_fact["fact"] if correct_fact else None,
                        legal_citations=[correct_fact["citation"]] if correct_fact else [],
                        official_sources=[correct_fact["source"]] if correct_fact else [],
                        explanation=f"This appears to be a common misconception. {correct_fact['fact'] if correct_fact else ''}",
                        confidence_score=0.8,
                        verification_method="static"
                    )
        
        # Check if it's a legal citation
        if claim.claim_type == LegalClaimType.LEGAL_CITATION:
            is_valid = self._verify_citation_format(claim.text)
            return VerificationResult(
                claim=claim,
                status=VerificationStatus.VERIFIED if is_valid else VerificationStatus.INCORRECT,
                explanation="Citation format is valid." if is_valid else "Citation format appears incorrect.",
                confidence_score=0.7,
                verification_method="static"
            )
        
        # Default to needs clarification
        return VerificationResult(
            claim=claim,
            status=VerificationStatus.NEEDS_CLARIFICATION,
            explanation="This claim requires additional context or verification.",
            confidence_score=0.4,
            verification_method="static"
        )
    
    async def _verify_claim_web(self, claim: LegalClaim) -> VerificationResult:
        """Verify a claim using web scraping of official sources"""
        if not self.jina_api_key:
            return VerificationResult(
                claim=claim,
                status=VerificationStatus.UNVERIFIABLE,
                explanation="Web verification not available.",
                confidence_score=0.3,
                verification_method="web"
            )
        
        try:
            # Search official ADA website
            search_query = quote(claim.text[:100])  # Limit query length
            ada_url = f"https://r.jina.ai/https://www.ada.gov/search/?q={search_query}"
            
            headers = {
                "Authorization": f"Bearer {self.jina_api_key}",
                "Accept": "application/json"
            }
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(ada_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Analyze content for verification
                    if self._content_supports_claim(content, claim.text):
                        return VerificationResult(
                            claim=claim,
                            status=VerificationStatus.VERIFIED,
                            explanation="Claim verified against ada.gov search results.",
                            confidence_score=0.75,
                            verification_method="web",
                            official_sources=["https://www.ada.gov"]
                        )
                    elif self._content_contradicts_claim(content, claim.text):
                        return VerificationResult(
                            claim=claim,
                            status=VerificationStatus.INCORRECT,
                            explanation="Claim contradicted by ada.gov search results.",
                            confidence_score=0.7,
                            verification_method="web",
                            official_sources=["https://www.ada.gov"]
                        )
        
        except Exception as e:
            logger.error(f"Web verification failed: {e}")
        
        return VerificationResult(
            claim=claim,
            status=VerificationStatus.UNVERIFIABLE,
            explanation="Could not verify claim through web sources.",
            confidence_score=0.3,
            verification_method="web"
        )
    
    def _check_claim_against_fact(self, claim_text: str, fact_data: Dict) -> bool:
        """Check if a claim is related to a specific fact"""
        fact_keywords = set(fact_data["fact"].lower().split())
        claim_keywords = set(claim_text.split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'is', 'are', 'and', 'or', 'to', 'of', 'in', 'for', 'be', 'has', 'have', 'may', 'can', 'must'}
        fact_keywords -= common_words
        claim_keywords -= common_words
        
        # Check for significant overlap
        overlap = len(fact_keywords & claim_keywords)
        if overlap >= min(3, len(fact_keywords) // 2):
            return True
        
        return False
    
    def _is_contradiction(self, claim_text: str, fact_data: Dict) -> bool:
        """Determine if a claim contradicts a known fact"""
        # Look for negation indicators
        contradictory_pairs = [
            ('must be registered', 'not require.*registration'),
            ('require.*certification', 'not require.*certification'),
            ('need.*identification', 'not require.*identification'),
            ('can ask for documentation', 'may.*not.*ask.*documentation'),
            ('emotional support.*same', 'not service animals'),
            ('professionally trained', 'not require.*professional')
        ]
        
        fact_text = fact_data["fact"].lower()
        
        for claim_pattern, fact_pattern in contradictory_pairs:
            if re.search(claim_pattern, claim_text) and re.search(fact_pattern, fact_text):
                return True
        
        # Check for explicit prohibitions in fact data
        if 'prohibited' in fact_data:
            for prohibited in fact_data['prohibited']:
                if prohibited.lower() in claim_text:
                    return True
        
        return False
    
    def _get_correct_fact_for_misconception_category(self, category: str) -> Optional[Dict]:
        """Get the correct fact that addresses a misconception category"""
        category_to_fact = {
            "registration_myths": self.ADA_FACTS_DATABASE["common_misconceptions"]["no_registration"],
            "identification_myths": self.ADA_FACTS_DATABASE["common_misconceptions"]["no_registration"],
            "documentation_myths": self.ADA_FACTS_DATABASE["business_requirements"]["two_questions"],
            "training_myths": self.ADA_FACTS_DATABASE["common_misconceptions"]["no_registration"],
            "esa_confusion": self.ADA_FACTS_DATABASE["common_misconceptions"]["emotional_support_difference"]
        }
        
        return category_to_fact.get(category)
    
    def _verify_citation_format(self, citation: str) -> bool:
        """Verify if a legal citation is correctly formatted"""
        for pattern in self.citation_patterns:
            if pattern.search(citation):
                return True
        return False
    
    def _content_supports_claim(self, content: str, claim: str) -> bool:
        """Check if web content supports a claim"""
        # Simple keyword matching (could be enhanced with NLP)
        claim_keywords = set(claim.lower().split())
        content_lower = content.lower()
        
        matching_keywords = sum(1 for keyword in claim_keywords if keyword in content_lower)
        
        return matching_keywords / len(claim_keywords) > 0.6
    
    def _content_contradicts_claim(self, content: str, claim: str) -> bool:
        """Check if web content contradicts a claim"""
        # Look for contradiction indicators
        if 'not' in content.lower() and any(word in claim.lower() for word in ['must', 'required', 'need']):
            return True
        
        return False
    
    def _check_compliance_violations(
        self,
        content: str,
        verification_results: List[VerificationResult]
    ) -> List[ComplianceViolation]:
        """Check for compliance violations in the content"""
        violations = []
        
        # Check for critical violations from incorrect claims
        for result in verification_results:
            if result.status == VerificationStatus.INCORRECT:
                severity = "critical" if "must" in result.claim.text.lower() else "high"
                violations.append(ComplianceViolation(
                    type="factual_error",
                    severity=severity,
                    description=f"Incorrect claim: {result.claim.text[:100]}",
                    regulation_reference=result.legal_citations[0] if result.legal_citations else None,
                    suggested_fix=result.correct_statement
                ))
        
        # Check for missing critical information
        content_lower = content.lower()
        
        if 'service animal' in content_lower or 'service dog' in content_lower:
            # Check if two questions are mentioned
            if 'two questions' not in content_lower and 'may ask only' not in content_lower:
                violations.append(ComplianceViolation(
                    type="missing_information",
                    severity="medium",
                    description="Article discusses service animals but doesn't mention the two questions rule",
                    regulation_reference="28 CFR §36.302(c)(6)",
                    suggested_fix="Include information about the two questions businesses may ask"
                ))
            
            # Check if no registration is mentioned
            if 'registration' in content_lower and 'not required' not in content_lower:
                violations.append(ComplianceViolation(
                    type="misleading_information",
                    severity="high",
                    description="Article mentions registration without clarifying it's not required",
                    regulation_reference="28 CFR §36.302(c)",
                    suggested_fix="Clarify that ADA does not require registration or certification"
                ))
        
        return violations
    
    def _check_comprehensive_disclaimers(self, content: str) -> List[str]:
        """Check for comprehensive disclaimers needed"""
        required_disclaimers = []
        content_lower = content.lower()
        
        # Medical advice disclaimer
        medical_terms = ['diagnosis', 'medical', 'treatment', 'therapy', 'medication', 'doctor', 'physician']
        if any(term in content_lower for term in medical_terms):
            if 'not medical advice' not in content_lower and 'informational purposes' not in content_lower:
                required_disclaimers.append(
                    "This article is for informational purposes only and does not constitute medical advice. "
                    "Always consult with qualified healthcare professionals regarding service dog needs."
                )
        
        # Legal advice disclaimer
        legal_terms = ['legal', 'rights', 'lawsuit', 'attorney', 'lawyer', 'court', 'sue']
        if any(term in content_lower for term in legal_terms):
            if 'not legal advice' not in content_lower:
                required_disclaimers.append(
                    "This article provides general information about the ADA and does not constitute legal advice. "
                    "For specific legal questions, consult with a qualified attorney specializing in disability law."
                )
        
        # State law variation disclaimer
        if 'state' in content_lower or 'local' in content_lower:
            if 'may vary' not in content_lower and 'additional' not in content_lower:
                required_disclaimers.append(
                    "State and local laws may provide additional protections beyond federal ADA requirements. "
                    "Check your local regulations for specific requirements in your area."
                )
        
        # Currency disclaimer
        if any(year in content_lower for year in ['2010', '2011', '2012', '2013', '2014', '2015']):
            required_disclaimers.append(
                "This article references regulations that may have been updated. "
                "Please verify current requirements at ada.gov for the most recent guidance."
            )
        
        # Training disclaimer
        if 'train' in content_lower and 'service dog' in content_lower:
            if 'consult' not in content_lower and 'professional' not in content_lower:
                required_disclaimers.append(
                    "Service dog training is complex and individualized. "
                    "Consider consulting with professional trainers experienced in service dog training."
                )
        
        return required_disclaimers
    
    def _generate_smart_corrections(self, results: List[VerificationResult]) -> List[Dict[str, Any]]:
        """Generate smart corrections with context"""
        corrections = []
        
        for result in results:
            if result.status == VerificationStatus.INCORRECT:
                correction = {
                    "original": result.claim.text,
                    "corrected": result.correct_statement or "Please verify this claim",
                    "explanation": result.explanation,
                    "citations": result.legal_citations,
                    "confidence": result.confidence_score,
                    "resources": result.official_sources
                }
                corrections.append(correction)
            
            elif result.status == VerificationStatus.PARTIALLY_CORRECT:
                correction = {
                    "original": result.claim.text,
                    "suggestion": "This claim needs clarification",
                    "explanation": result.explanation,
                    "citations": result.legal_citations,
                    "confidence": result.confidence_score
                }
                corrections.append(correction)
            
            elif result.status == VerificationStatus.NEEDS_CLARIFICATION:
                correction = {
                    "original": result.claim.text,
                    "suggestion": "Add more specific details or context",
                    "explanation": "This claim is too vague or ambiguous to verify",
                    "confidence": result.confidence_score
                }
                corrections.append(correction)
        
        return corrections
    
    def _generate_report_summary(
        self,
        accuracy_score: float,
        compliance_score: float,
        verified: int,
        incorrect: int,
        partial: int,
        total: int
    ) -> str:
        """Generate a comprehensive report summary"""
        grade = self._calculate_grade(accuracy_score, compliance_score)
        
        summary = f"""
Legal Fact-Check Report Summary
================================
Overall Grade: {grade}
Accuracy Score: {accuracy_score:.1%}
Compliance Score: {compliance_score:.1%}

Claims Analysis:
- Total Claims Checked: {total}
- Verified as Correct: {verified} ({verified/max(1,total):.1%})
- Incorrect Claims: {incorrect} ({incorrect/max(1,total):.1%})
- Partially Correct: {partial} ({partial/max(1,total):.1%})

"""
        
        if accuracy_score < 0.8:
            summary += "⚠️ WARNING: This article contains significant factual errors that should be corrected before publication.\n"
        
        if compliance_score < 0.7:
            summary += "⚠️ COMPLIANCE ALERT: This article has compliance issues that could pose legal risks.\n"
        
        if accuracy_score >= 0.9 and compliance_score >= 0.9:
            summary += "✅ EXCELLENT: This article meets high standards for accuracy and compliance.\n"
        
        return summary
    
    def _calculate_grade(self, accuracy_score: float, compliance_score: float) -> str:
        """Calculate letter grade based on scores"""
        combined_score = (accuracy_score + compliance_score) / 2
        
        if combined_score >= 0.95:
            return "A+"
        elif combined_score >= 0.90:
            return "A"
        elif combined_score >= 0.85:
            return "B+"
        elif combined_score >= 0.80:
            return "B"
        elif combined_score >= 0.75:
            return "C+"
        elif combined_score >= 0.70:
            return "C"
        elif combined_score >= 0.65:
            return "D"
        else:
            return "F"
    
    async def generate_legal_disclaimer(
        self,
        content_type: str,
        article_content: Optional[str] = None
    ) -> str:
        """Generate appropriate legal disclaimer based on content"""
        disclaimers = {
            "general": """
LEGAL DISCLAIMER: This article is provided for informational and educational purposes only and does not constitute legal or medical advice. The information presented is based on the Americans with Disabilities Act (ADA) as of the publication date. Laws and regulations may change, and individual circumstances vary. Always consult with qualified professionals for advice specific to your situation.
""",
            "service_dog_training": """
SERVICE DOG TRAINING DISCLAIMER: The information in this article about service dog training is for educational purposes only. Service dog training should be tailored to the individual's specific disability-related needs. This content does not replace professional training guidance or medical advice about whether a service dog is appropriate for your condition. Consult with healthcare providers and experienced service dog trainers for personalized guidance.
""",
            "ada_compliance": """
ADA COMPLIANCE NOTE: This article discusses requirements under the Americans with Disabilities Act (ADA) based on current federal regulations. State and local laws may provide additional protections. This information is not exhaustive and does not constitute legal advice. For specific compliance questions, consult with an attorney specializing in disability law or contact the Department of Justice ADA Information Line at 800-514-0301.
""",
            "business_guidance": """
BUSINESS GUIDANCE DISCLAIMER: This article provides general guidance for businesses regarding ADA compliance. It is not a substitute for legal counsel. Each business situation is unique, and specific circumstances may require different approaches. Businesses should consult with legal professionals familiar with ADA requirements and any applicable state or local laws. For official guidance, refer to ada.gov or contact the Department of Justice.
""",
            "medical_aspects": """
MEDICAL DISCLAIMER: This article contains information about medical conditions and disabilities in relation to service dogs. This information is for educational purposes only and should not be used for self-diagnosis or treatment decisions. The determination of whether you have a qualifying disability under the ADA and whether a service dog would be beneficial must be made by qualified healthcare professionals familiar with your specific situation.
"""
        }
        
        # If article content provided, analyze it to determine appropriate disclaimer
        if article_content:
            content_lower = article_content.lower()
            selected_disclaimers = []
            
            if 'train' in content_lower and 'service dog' in content_lower:
                selected_disclaimers.append(disclaimers["service_dog_training"])
            
            if 'business' in content_lower or 'employer' in content_lower:
                selected_disclaimers.append(disclaimers["business_guidance"])
            
            if any(term in content_lower for term in ['medical', 'diagnosis', 'condition', 'disability']):
                selected_disclaimers.append(disclaimers["medical_aspects"])
            
            if 'ada' in content_lower or 'compliance' in content_lower:
                selected_disclaimers.append(disclaimers["ada_compliance"])
            
            if not selected_disclaimers:
                selected_disclaimers.append(disclaimers["general"])
            
            return "\n".join(selected_disclaimers)
        
        # Return specific disclaimer if type provided
        return disclaimers.get(content_type, disclaimers["general"])


# Convenience function for backward compatibility
async def create_fact_checker(
    research_dir: Optional[str] = None,
    enable_web: bool = True
) -> EnhancedLegalFactCheckerAgent:
    """Create and return an enhanced fact checker instance"""
    return EnhancedLegalFactCheckerAgent(
        research_dir=research_dir or "research/legal/ada-official",
        enable_web_verification=enable_web
    )