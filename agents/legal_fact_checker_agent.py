"""
Legal Fact Checker Agent
Verifies ADA compliance claims and legal accuracy using official sources
"""
import os
import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field

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


class VerificationStatus(str, Enum):
    """Verification status for claims"""
    VERIFIED = "verified"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    NEEDS_CLARIFICATION = "needs_clarification"
    UNVERIFIABLE = "unverifiable"


class LegalClaim(BaseModel):
    """Individual legal claim to verify"""
    text: str
    claim_type: LegalClaimType
    context: Optional[str] = None
    source_paragraph: Optional[str] = None


class VerificationResult(BaseModel):
    """Result of verifying a legal claim"""
    claim: LegalClaim
    status: VerificationStatus
    correct_statement: Optional[str] = None
    legal_citations: List[str] = Field(default_factory=list)
    official_sources: List[str] = Field(default_factory=list)
    explanation: str
    confidence_score: float = Field(ge=0.0, le=1.0)


class LegalFactCheckReport(BaseModel):
    """Complete fact-checking report for an article"""
    article_title: str
    total_claims: int
    verified_claims: int
    incorrect_claims: int
    partially_correct_claims: int
    verification_results: List[VerificationResult]
    required_disclaimers: List[str]
    suggested_corrections: List[Dict[str, str]]
    overall_accuracy_score: float = Field(ge=0.0, le=1.0)
    checked_at: datetime = Field(default_factory=datetime.now)


class LegalFactCheckerAgent:
    """
    Agent responsible for verifying legal accuracy of ADA-related content
    """
    
    # Core ADA facts from official sources
    ADA_FACTS = {
        "two_questions": {
            "fact": "Staff may ask only two questions: (1) is the dog a service animal required because of a disability, and (2) what work or task has the dog been trained to perform.",
            "citation": "28 CFR §36.302(c)(6)",
            "source": "https://www.ada.gov/resources/service-animals-faqs/"
        },
        "no_registration": {
            "fact": "The ADA does not require service animals to be registered, certified, or have any special identification.",
            "citation": "28 CFR §36.302(c)",
            "source": "https://www.ada.gov/resources/service-animals-2010-requirements/"
        },
        "definition": {
            "fact": "Service animals are defined as dogs that are individually trained to do work or perform tasks for people with disabilities.",
            "citation": "28 CFR §36.302(c)(1)",
            "source": "https://www.ada.gov/resources/service-animals-2010-requirements/"
        },
        "miniature_horses": {
            "fact": "Miniature horses may be permitted as service animals under specific conditions outlined in the regulations.",
            "citation": "28 CFR §36.302(c)(9)",
            "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302"
        },
        "no_breed_restrictions": {
            "fact": "The ADA does not restrict the type of dog breeds that can be service animals.",
            "citation": "28 CFR §36.302(c)",
            "source": "https://www.ada.gov/resources/service-animals-faqs/"
        },
        "handler_responsibilities": {
            "fact": "The handler is responsible for caring for and supervising the service animal, including toileting, feeding, grooming and veterinary care.",
            "citation": "28 CFR §36.302(c)(5)",
            "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302"
        },
        "no_surcharge": {
            "fact": "People with disabilities who use service animals cannot be charged extra fees, isolated from other patrons, or treated less favorably.",
            "citation": "28 CFR §36.302(c)(8)",
            "source": "https://www.ada.gov/resources/service-animals-faqs/"
        },
        "removal_conditions": {
            "fact": "A service animal may be removed if it is out of control and the handler does not take effective action, or if it is not housebroken.",
            "citation": "28 CFR §36.302(c)(2)",
            "source": "https://www.ecfr.gov/current/title-28/chapter-I/part-36/section-36.302"
        },
        "work_or_task": {
            "fact": "The work or task must be directly related to the person's disability. Emotional support alone does not qualify.",
            "citation": "28 CFR §36.302(c)(1)",
            "source": "https://www.ada.gov/resources/service-animals-faqs/"
        },
        "public_accommodations": {
            "fact": "Service animals are allowed in all areas of public accommodations where members of the public are allowed to go.",
            "citation": "28 CFR §36.302(c)(7)",
            "source": "https://www.ada.gov/resources/service-animals-2010-requirements/"
        }
    }
    
    # Common misconceptions to check for
    COMMON_MISCONCEPTIONS = {
        "registration_required": "Service dogs must be registered or certified",
        "vest_required": "Service dogs must wear a vest or special identification",
        "documentation_allowed": "Businesses can ask for documentation or proof of disability",
        "esa_same_as_service": "Emotional support animals have the same rights as service animals",
        "training_certification": "Service dogs must be professionally trained or certified",
        "breed_restrictions": "Certain breeds cannot be service dogs",
        "size_restrictions": "Service dogs must be a certain size",
        "age_restrictions": "Service dogs must be a certain age",
        "multiple_dogs": "A person can only have one service dog",
        "pet_fees": "Service dogs can be charged pet fees or deposits"
    }
    
    def __init__(self, research_dir: str = "research/legal/ada-official"):
        """
        Initialize the legal fact checker agent
        
        Args:
            research_dir: Directory containing ADA research documents
        """
        self.research_dir = Path(research_dir)
        self.legal_sources = self._load_legal_sources()
        self.citation_patterns = [
            r'\d+\s+CFR\s+§?\s*\d+\.\d+',  # Federal regulations
            r'28\s+CFR\s+(Part\s+)?\d+',    # Title 28 CFR
            r'ADA\s+Title\s+[IVX]+',        # ADA Titles
            r'DOJ\s+guidance',               # DOJ guidance references
            r'§\s*\d+\.\d+'                  # Section references
        ]
    
    def _load_legal_sources(self) -> Dict[str, str]:
        """Load ADA research documents from disk"""
        sources = {}
        
        if not self.research_dir.exists():
            logger.warning(f"Research directory not found: {self.research_dir}")
            return sources
        
        # Load all markdown files from research directory
        for md_file in self.research_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Store by relative path for easy reference
                    rel_path = md_file.relative_to(self.research_dir)
                    sources[str(rel_path)] = content
                    logger.info(f"Loaded legal source: {rel_path}")
            except Exception as e:
                logger.error(f"Failed to load {md_file}: {e}")
        
        logger.info(f"Loaded {len(sources)} legal source documents")
        return sources
    
    async def fact_check_article(
        self,
        article_content: str,
        article_title: str = "Untitled Article",
        check_citations: bool = True,
        check_claims: bool = True,
        suggest_corrections: bool = True
    ) -> LegalFactCheckReport:
        """
        Perform comprehensive fact-checking on an article
        
        Args:
            article_content: The article text to check
            article_title: Title of the article
            check_citations: Whether to verify legal citations
            check_claims: Whether to verify factual claims
            suggest_corrections: Whether to suggest corrections
        
        Returns:
            LegalFactCheckReport with all verification results
        """
        # Extract claims from the article
        claims = self._extract_claims(article_content)
        
        # Verify each claim
        verification_results = []
        for claim in claims:
            result = await self._verify_claim(claim)
            verification_results.append(result)
        
        # Check for required disclaimers
        disclaimers = self._check_disclaimers(article_content)
        
        # Generate corrections if requested
        corrections = []
        if suggest_corrections:
            corrections = self._generate_corrections(verification_results)
        
        # Calculate overall accuracy
        verified = sum(1 for r in verification_results if r.status == VerificationStatus.VERIFIED)
        incorrect = sum(1 for r in verification_results if r.status == VerificationStatus.INCORRECT)
        partial = sum(1 for r in verification_results if r.status == VerificationStatus.PARTIALLY_CORRECT)
        
        total = len(verification_results)
        accuracy_score = (verified + (partial * 0.5)) / max(1, total)
        
        return LegalFactCheckReport(
            article_title=article_title,
            total_claims=total,
            verified_claims=verified,
            incorrect_claims=incorrect,
            partially_correct_claims=partial,
            verification_results=verification_results,
            required_disclaimers=disclaimers,
            suggested_corrections=corrections,
            overall_accuracy_score=accuracy_score
        )
    
    def _extract_claims(self, content: str) -> List[LegalClaim]:
        """Extract legal claims from article content"""
        claims = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]\s+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check for ADA-related keywords
            ada_keywords = [
                'ADA', 'service dog', 'service animal', 'disability',
                'handler', 'business', 'public accommodation', 'access',
                'registration', 'certification', 'vest', 'identification',
                'trained', 'task', 'work', 'emotional support', 'ESA',
                'required', 'allowed', 'must', 'cannot', 'may not',
                'two questions', 'ask', 'proof', 'documentation'
            ]
            
            sentence_lower = sentence.lower()
            if any(keyword.lower() in sentence_lower for keyword in ada_keywords):
                # Determine claim type
                claim_type = self._determine_claim_type(sentence)
                
                claims.append(LegalClaim(
                    text=sentence,
                    claim_type=claim_type,
                    context=None  # Could add surrounding sentences for context
                ))
        
        # Also extract citations
        citations = re.findall(r'(' + '|'.join(self.citation_patterns) + r')', content)
        for citation in citations:
            claims.append(LegalClaim(
                text=f"Citation: {citation}",
                claim_type=LegalClaimType.LEGAL_CITATION
            ))
        
        return claims
    
    def _determine_claim_type(self, sentence: str) -> LegalClaimType:
        """Determine the type of legal claim"""
        sentence_lower = sentence.lower()
        
        if 'service animal' in sentence_lower or 'service dog' in sentence_lower:
            if 'definition' in sentence_lower or 'defined as' in sentence_lower:
                return LegalClaimType.SERVICE_ANIMAL_RULE
            elif 'registration' in sentence_lower or 'certification' in sentence_lower:
                return LegalClaimType.REGISTRATION_CLAIM
        
        if 'business' in sentence_lower or 'ask' in sentence_lower or 'require' in sentence_lower:
            return LegalClaimType.BUSINESS_OBLIGATION
        
        if 'handler' in sentence_lower or 'owner' in sentence_lower:
            return LegalClaimType.HANDLER_RIGHT
        
        if 'access' in sentence_lower or 'allowed' in sentence_lower or 'admission' in sentence_lower:
            return LegalClaimType.ACCESS_RIGHT
        
        if 'remove' in sentence_lower or 'exclude' in sentence_lower or 'deny' in sentence_lower:
            return LegalClaimType.EXCLUSION_RULE
        
        if re.search(r'\d+\s+CFR', sentence) or 'ADA' in sentence:
            return LegalClaimType.LEGAL_CITATION
        
        return LegalClaimType.ADA_REQUIREMENT
    
    async def _verify_claim(self, claim: LegalClaim) -> VerificationResult:
        """Verify an individual claim against ADA facts"""
        claim_lower = claim.text.lower()
        
        # Check against known facts
        for fact_key, fact_data in self.ADA_FACTS.items():
            fact_text = fact_data["fact"].lower()
            
            # Check for direct contradictions
            if self._check_contradiction(claim_lower, fact_text):
                return VerificationResult(
                    claim=claim,
                    status=VerificationStatus.INCORRECT,
                    correct_statement=fact_data["fact"],
                    legal_citations=[fact_data["citation"]],
                    official_sources=[fact_data["source"]],
                    explanation=f"This claim contradicts official ADA guidance. {fact_data['fact']}",
                    confidence_score=0.95
                )
            
            # Check for alignment
            if self._check_alignment(claim_lower, fact_text):
                return VerificationResult(
                    claim=claim,
                    status=VerificationStatus.VERIFIED,
                    correct_statement=None,
                    legal_citations=[fact_data["citation"]],
                    official_sources=[fact_data["source"]],
                    explanation="This claim is consistent with official ADA requirements.",
                    confidence_score=0.90
                )
        
        # Check against common misconceptions
        for misconception_key, misconception_text in self.COMMON_MISCONCEPTIONS.items():
            if self._check_misconception(claim_lower, misconception_text.lower()):
                # Find the correct fact
                correct_fact = self._get_correct_fact_for_misconception(misconception_key)
                return VerificationResult(
                    claim=claim,
                    status=VerificationStatus.INCORRECT,
                    correct_statement=correct_fact["fact"] if correct_fact else None,
                    legal_citations=[correct_fact["citation"]] if correct_fact else [],
                    official_sources=[correct_fact["source"]] if correct_fact else [],
                    explanation=f"This is a common misconception about service animals. {correct_fact['fact'] if correct_fact else ''}",
                    confidence_score=0.85
                )
        
        # Check legal citations
        if claim.claim_type == LegalClaimType.LEGAL_CITATION:
            is_valid = self._verify_citation(claim.text)
            return VerificationResult(
                claim=claim,
                status=VerificationStatus.VERIFIED if is_valid else VerificationStatus.INCORRECT,
                correct_statement=None,
                legal_citations=[],
                official_sources=[],
                explanation="Citation format is valid." if is_valid else "Citation format appears incorrect.",
                confidence_score=0.80
            )
        
        # If we can't definitively verify, mark as needs clarification
        return VerificationResult(
            claim=claim,
            status=VerificationStatus.NEEDS_CLARIFICATION,
            correct_statement=None,
            legal_citations=[],
            official_sources=[],
            explanation="This claim could not be definitively verified against official sources.",
            confidence_score=0.50
        )
    
    def _check_contradiction(self, claim: str, fact: str) -> bool:
        """Check if a claim contradicts a known fact"""
        # Look for negation patterns
        negation_patterns = [
            (r'must\s+be\s+registered', r'not\s+require.*registration'),
            (r'require.*certification', r'not\s+require.*certification'),
            (r'can\s+ask\s+for\s+documentation', r'may\s+not\s+ask.*documentation'),
            (r'emotional\s+support.*same\s+rights', r'emotional\s+support.*not\s+qualify'),
        ]
        
        for claim_pattern, fact_pattern in negation_patterns:
            if re.search(claim_pattern, claim) and re.search(fact_pattern, fact):
                return True
        
        return False
    
    def _check_alignment(self, claim: str, fact: str) -> bool:
        """Check if a claim aligns with a known fact"""
        # Simple keyword overlap check (could be made more sophisticated)
        claim_words = set(claim.split())
        fact_words = set(fact.split())
        
        # Remove common words
        common_words = {'the', 'a', 'an', 'is', 'are', 'and', 'or', 'to', 'of', 'in', 'for'}
        claim_words -= common_words
        fact_words -= common_words
        
        # Calculate overlap
        overlap = len(claim_words & fact_words)
        min_length = min(len(claim_words), len(fact_words))
        
        if min_length > 0:
            similarity = overlap / min_length
            return similarity > 0.5
        
        return False
    
    def _check_misconception(self, claim: str, misconception: str) -> bool:
        """Check if a claim contains a common misconception"""
        misconception_words = set(misconception.split())
        claim_words = set(claim.split())
        
        # Check for key misconception indicators
        if len(misconception_words & claim_words) / len(misconception_words) > 0.6:
            return True
        
        return False
    
    def _get_correct_fact_for_misconception(self, misconception_key: str) -> Optional[Dict[str, str]]:
        """Get the correct fact that addresses a misconception"""
        misconception_to_fact = {
            "registration_required": "no_registration",
            "vest_required": "no_registration",
            "documentation_allowed": "two_questions",
            "esa_same_as_service": "work_or_task",
            "training_certification": "no_registration",
            "breed_restrictions": "no_breed_restrictions",
            "pet_fees": "no_surcharge"
        }
        
        fact_key = misconception_to_fact.get(misconception_key)
        if fact_key:
            return self.ADA_FACTS.get(fact_key)
        
        return None
    
    def _verify_citation(self, citation: str) -> bool:
        """Verify if a legal citation is correctly formatted"""
        # Check against known citation patterns
        for pattern in self.citation_patterns:
            if re.search(pattern, citation):
                return True
        return False
    
    def _check_disclaimers(self, content: str) -> List[str]:
        """Check for required disclaimers and suggest missing ones"""
        required_disclaimers = []
        content_lower = content.lower()
        
        # Check if article discusses medical or legal advice
        if 'diagnosis' in content_lower or 'medical' in content_lower:
            if 'not medical advice' not in content_lower:
                required_disclaimers.append(
                    "This article is for informational purposes only and does not constitute medical advice."
                )
        
        if 'legal' in content_lower or 'rights' in content_lower:
            if 'not legal advice' not in content_lower:
                required_disclaimers.append(
                    "This article provides general information and does not constitute legal advice. "
                    "Consult with a qualified attorney for specific legal questions."
                )
        
        # Check if article mentions state laws
        if 'state law' in content_lower or 'local law' in content_lower:
            if 'may vary' not in content_lower:
                required_disclaimers.append(
                    "State and local laws may provide additional protections beyond federal ADA requirements."
                )
        
        return required_disclaimers
    
    def _generate_corrections(self, results: List[VerificationResult]) -> List[Dict[str, str]]:
        """Generate suggested corrections for incorrect claims"""
        corrections = []
        
        for result in results:
            if result.status == VerificationStatus.INCORRECT and result.correct_statement:
                corrections.append({
                    "original": result.claim.text,
                    "corrected": result.correct_statement,
                    "explanation": result.explanation,
                    "citations": result.legal_citations
                })
            elif result.status == VerificationStatus.PARTIALLY_CORRECT:
                corrections.append({
                    "original": result.claim.text,
                    "suggestion": "Consider clarifying this statement",
                    "explanation": result.explanation,
                    "citations": result.legal_citations
                })
        
        return corrections
    
    async def verify_single_claim(self, claim_text: str) -> VerificationResult:
        """Verify a single claim text"""
        claim = LegalClaim(
            text=claim_text,
            claim_type=self._determine_claim_type(claim_text)
        )
        return await self._verify_claim(claim)
    
    def get_ada_facts_summary(self) -> Dict[str, Any]:
        """Get a summary of key ADA facts for reference"""
        return {
            "key_facts": [fact_data["fact"] for fact_data in self.ADA_FACTS.values()],
            "common_misconceptions": list(self.COMMON_MISCONCEPTIONS.values()),
            "official_sources": list(set(
                fact_data["source"] for fact_data in self.ADA_FACTS.values()
            ))
        }


# Example usage
async def main():
    """Example of using the legal fact checker agent"""
    
    # Initialize agent
    agent = LegalFactCheckerAgent()
    
    # Example article content to check
    article_content = """
    Service dogs must be registered with the ADA before they can enter public spaces.
    Business owners can ask handlers to provide documentation proving their disability.
    Under the ADA, businesses may only ask two questions: Is this a service animal? 
    And what work or task has the dog been trained to perform?
    Emotional support animals have the same access rights as service dogs.
    Service dogs must wear a vest to be recognized.
    """
    
    # Perform fact checking
    report = await agent.fact_check_article(
        article_content=article_content,
        article_title="Understanding Service Dog Rights"
    )
    
    print(f"Fact Check Report for: {report.article_title}")
    print(f"Overall Accuracy Score: {report.overall_accuracy_score:.1%}")
    print(f"Total Claims: {report.total_claims}")
    print(f"Verified: {report.verified_claims}")
    print(f"Incorrect: {report.incorrect_claims}")
    
    print("\nIncorrect Claims Found:")
    for result in report.verification_results:
        if result.status == VerificationStatus.INCORRECT:
            print(f"❌ {result.claim.text}")
            print(f"   Correction: {result.correct_statement}")
            print(f"   Citation: {', '.join(result.legal_citations)}")
    
    print("\nRequired Disclaimers:")
    for disclaimer in report.required_disclaimers:
        print(f"⚠️ {disclaimer}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())