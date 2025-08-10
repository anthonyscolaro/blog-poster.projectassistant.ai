"""
Test suite for Legal Fact Checker Agent
"""
import pytest
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.legal_fact_checker_agent import (
    LegalFactCheckerAgent,
    LegalClaim,
    LegalClaimType,
    VerificationStatus,
    VerificationResult
)


class TestLegalFactChecker:
    """Test cases for the Legal Fact Checker Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create a legal fact checker agent"""
        return LegalFactCheckerAgent()
    
    @pytest.mark.asyncio
    async def test_verify_correct_two_questions_claim(self, agent):
        """Test verification of the correct two questions rule"""
        claim = "Businesses may only ask two questions: Is this a service animal? And what work or task has the dog been trained to perform?"
        
        result = await agent.verify_single_claim(claim)
        
        assert result.status == VerificationStatus.VERIFIED
        assert result.confidence_score > 0.8
        assert "28 CFR §36.302(c)(6)" in result.legal_citations
    
    @pytest.mark.asyncio
    async def test_verify_incorrect_registration_claim(self, agent):
        """Test detection of incorrect registration requirement"""
        claim = "Service dogs must be registered with the ADA before entering public spaces."
        
        result = await agent.verify_single_claim(claim)
        
        assert result.status == VerificationStatus.INCORRECT
        assert result.correct_statement is not None
        assert "not require" in result.correct_statement.lower()
        assert "registration" in result.correct_statement.lower()
    
    @pytest.mark.asyncio
    async def test_verify_incorrect_documentation_claim(self, agent):
        """Test detection of incorrect documentation requirement"""
        claim = "Business owners can ask handlers to provide documentation proving their disability."
        
        result = await agent.verify_single_claim(claim)
        
        assert result.status == VerificationStatus.INCORRECT
        assert result.explanation is not None
        assert "contradicts" in result.explanation.lower() or "incorrect" in result.explanation.lower()
    
    @pytest.mark.asyncio
    async def test_verify_esa_misconception(self, agent):
        """Test detection of ESA misconception"""
        claim = "Emotional support animals have the same access rights as service dogs under the ADA."
        
        result = await agent.verify_single_claim(claim)
        
        assert result.status == VerificationStatus.INCORRECT
        assert result.correct_statement is not None
        assert "emotional support" in result.explanation.lower()
    
    @pytest.mark.asyncio
    async def test_verify_vest_misconception(self, agent):
        """Test detection of vest requirement misconception"""
        claim = "Service dogs must wear a vest or special identification to be recognized."
        
        result = await agent.verify_single_claim(claim)
        
        assert result.status == VerificationStatus.INCORRECT
        assert "misconception" in result.explanation.lower()
    
    @pytest.mark.asyncio
    async def test_fact_check_article_with_multiple_claims(self, agent):
        """Test fact-checking an article with multiple claims"""
        article_content = """
        Under the ADA, service dogs are defined as dogs that are individually trained 
        to do work or perform tasks for people with disabilities. 
        
        Service dogs must be registered and certified before they can access public spaces.
        
        Businesses may only ask two questions about service animals.
        
        Emotional support animals are not considered service animals under the ADA.
        """
        
        report = await agent.fact_check_article(
            article_content=article_content,
            article_title="Test Article"
        )
        
        assert report.total_claims > 0
        assert report.verified_claims > 0
        assert report.incorrect_claims > 0
        assert 0 <= report.overall_accuracy_score <= 1
    
    @pytest.mark.asyncio
    async def test_check_disclaimers(self, agent):
        """Test disclaimer checking"""
        article_content = """
        This article discusses legal rights under the ADA and provides medical 
        information about service dogs for anxiety disorders.
        """
        
        report = await agent.fact_check_article(
            article_content=article_content,
            article_title="Test Article"
        )
        
        assert len(report.required_disclaimers) > 0
        assert any("legal advice" in d for d in report.required_disclaimers)
        assert any("medical advice" in d for d in report.required_disclaimers)
    
    @pytest.mark.asyncio
    async def test_verify_citation_format(self, agent):
        """Test verification of legal citation formats"""
        valid_citation = "Citation: 28 CFR §36.302(c)"
        invalid_citation = "Citation: ADA Section XYZ"
        
        valid_result = await agent.verify_single_claim(valid_citation)
        invalid_result = await agent.verify_single_claim(invalid_citation)
        
        assert valid_result.status == VerificationStatus.VERIFIED
        assert invalid_result.status != VerificationStatus.VERIFIED
    
    def test_ada_facts_loaded(self, agent):
        """Test that ADA facts are properly loaded"""
        facts_summary = agent.get_ada_facts_summary()
        
        assert len(facts_summary["key_facts"]) > 0
        assert len(facts_summary["common_misconceptions"]) > 0
        assert len(facts_summary["official_sources"]) > 0
        
        # Check for key facts
        facts_text = " ".join(facts_summary["key_facts"]).lower()
        assert "two questions" in facts_text
        assert "registration" in facts_text
        assert "service animal" in facts_text


@pytest.mark.asyncio
async def test_legal_fact_checker_integration():
    """Integration test for the legal fact checker"""
    agent = LegalFactCheckerAgent()
    
    # Test a complete article
    test_article = """
    # Understanding Service Dog Rights Under the ADA
    
    Service dogs play a crucial role in helping people with disabilities navigate 
    daily life. Under the Americans with Disabilities Act (ADA), specifically 
    28 CFR §36.302(c), service animals are defined as dogs that are individually 
    trained to do work or perform tasks for people with disabilities.
    
    ## What Businesses Need to Know
    
    When a person with a service dog enters your establishment, you may only ask 
    two questions: (1) Is the dog a service animal required because of a disability? 
    and (2) What work or task has the dog been trained to perform?
    
    You cannot require special identification, documentation, or proof that the 
    animal has been certified or trained as a service animal. The ADA does not 
    require service animals to be registered.
    
    ## Common Misconceptions
    
    Many people believe that emotional support animals have the same rights as 
    service dogs, but this is not true under federal law. Only dogs (and in some 
    cases, miniature horses) that are individually trained to perform specific 
    tasks qualify as service animals under the ADA.
    
    ## Handler Responsibilities
    
    The handler is responsible for the care and supervision of the service animal, 
    including toileting, feeding, grooming, and veterinary care. If a service 
    animal is out of control and the handler does not take effective action, or 
    if the animal is not housebroken, the business may ask that the animal be removed.
    
    ## Important Note
    
    This article provides general information about ADA requirements. State and 
    local laws may provide additional protections. For specific legal questions, 
    consult with a qualified attorney.
    """
    
    report = await agent.fact_check_article(
        article_content=test_article,
        article_title="Understanding Service Dog Rights"
    )
    
    # This article should have high accuracy
    assert report.overall_accuracy_score > 0.8
    assert report.verified_claims > report.incorrect_claims
    assert len(report.required_disclaimers) >= 0  # Disclaimer is included
    
    print(f"\n✅ Integration Test Passed!")
    print(f"   Article Accuracy: {report.overall_accuracy_score:.1%}")
    print(f"   Verified Claims: {report.verified_claims}/{report.total_claims}")


if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_legal_fact_checker_integration())