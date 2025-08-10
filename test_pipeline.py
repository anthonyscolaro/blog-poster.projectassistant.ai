#!/usr/bin/env python3
"""
Test the complete multi-agent pipeline orchestration
"""
import asyncio
import httpx
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')


async def test_pipeline():
    """Test the complete pipeline via API"""
    base_url = "http://localhost:8088"
    
    print("=" * 60)
    print("🚀 Testing Complete Multi-Agent Pipeline")
    print("=" * 60)
    print("\nThis will orchestrate all 5 agents:")
    print("1. Competitor Monitoring")
    print("2. Topic Analysis")
    print("3. Article Generation")
    print("4. Legal Fact Checking")
    print("5. WordPress Publishing")
    print("=" * 60)
    
    # Pipeline configuration
    config = {
        "topic": "Service Dog Training for Anxiety Disorders",
        "primary_keyword": "anxiety service dog",
        "secondary_keywords": [
            "service dog training",
            "anxiety support",
            "ADA requirements",
            "psychiatric service dog"
        ],
        "min_words": 1500,
        "max_words": 2000,
        "use_competitor_insights": True,
        "perform_fact_checking": True,
        "auto_publish": True,  # Will publish to WordPress
        "publish_status": "draft",  # Keep as draft
        "max_cost_per_article": 0.50
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # Run the pipeline
            print(f"\n⏳ Starting pipeline at {datetime.now().strftime('%H:%M:%S')}")
            print(f"Topic: {config['topic']}")
            print(f"Keywords: {config['primary_keyword']}, {', '.join(config['secondary_keywords'][:2])}")
            print("\nThis may take 30-60 seconds...\n")
            
            response = await client.post(
                f"{base_url}/pipeline/run",
                json=config
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print("✅ Pipeline completed successfully!")
                print("=" * 60)
                
                # Display results
                print(f"\n📊 Execution Summary:")
                print(f"   Status: {result['status']}")
                print(f"   Time: {result['execution_time']:.2f} seconds")
                print(f"   Cost: ${result['total_cost']:.4f}")
                
                # Article details
                if 'article' in result:
                    print(f"\n📝 Generated Article:")
                    print(f"   Title: {result['article']['title']}")
                    print(f"   Word Count: {result['article']['word_count']}")
                    print(f"   SEO Score: {result['article']['seo_score']}/100")
                    print(f"   Slug: {result['article']['slug']}")
                
                # Fact check results
                if 'fact_check' in result:
                    fc = result['fact_check']
                    print(f"\n✅ Legal Fact Check:")
                    print(f"   Accuracy: {fc['accuracy_score']:.1%}")
                    print(f"   Claims Verified: {fc['verified_claims']}/{fc['total_claims']}")
                    print(f"   Incorrect Claims: {fc['incorrect_claims']}")
                
                # WordPress publishing
                if 'wordpress' in result:
                    wp = result['wordpress']
                    print(f"\n🌐 WordPress Publishing:")
                    print(f"   Post ID: {wp['post_id']}")
                    print(f"   Edit Link: {wp['edit_link']}")
                    if wp.get('view_link'):
                        print(f"   View Link: {wp['view_link']}")
                
                # Errors/warnings
                if result.get('errors'):
                    print(f"\n❌ Errors:")
                    for error in result['errors']:
                        print(f"   - {error}")
                
                if result.get('warnings'):
                    print(f"\n⚠️ Warnings:")
                    for warning in result['warnings']:
                        print(f"   - {warning}")
                
            else:
                print(f"❌ Pipeline failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except httpx.TimeoutException:
            print("❌ Request timed out. Pipeline may still be running.")
            print("Check status at: GET /pipeline/status")
        except Exception as e:
            print(f"❌ Error: {e}")


async def check_pipeline_status():
    """Check current pipeline status"""
    base_url = "http://localhost:8088"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/pipeline/status")
        status = response.json()
        
        print("\n📊 Pipeline Status:")
        if status['running']:
            print(f"   ✅ Running: {status['status']}")
            print(f"   {status['message']}")
        else:
            print(f"   ⏸️ Not running")


async def get_pipeline_history():
    """Get pipeline execution history"""
    base_url = "http://localhost:8088"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/pipeline/history?limit=5")
        history = response.json()
        
        print("\n📜 Recent Pipeline Executions:")
        for i, execution in enumerate(history['executions'], 1):
            print(f"\n   {i}. Status: {execution['status']}")
            print(f"      Started: {execution['started_at']}")
            if execution['completed_at']:
                print(f"      Completed: {execution['completed_at']}")
            print(f"      Duration: {execution['execution_time']:.2f}s")
            print(f"      Cost: ${execution['total_cost']:.4f}")
            if execution['errors']:
                print(f"      Errors: {', '.join(execution['errors'][:2])}")


async def get_cost_summary():
    """Get cost summary"""
    base_url = "http://localhost:8088"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/pipeline/costs")
        costs = response.json()
        
        print("\n💰 Cost Summary:")
        print(f"   Total Cost: ${costs['total_cost']:.4f}")
        print(f"   Average Cost: ${costs['average_cost']:.4f}")
        print(f"   Executions: {costs['executions']}")


async def main():
    """Main test function"""
    print("\n🔧 Blog Poster Pipeline Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8088/health")
            if response.status_code != 200:
                print("❌ Server is not healthy. Please start it first:")
                print("   docker compose up -d")
                print("   uvicorn app:app --reload --port 8088")
                return
    except:
        print("❌ Cannot connect to server at http://localhost:8088")
        print("   Please start the server first:")
        print("   docker compose up -d")
        print("   uvicorn app:app --reload --port 8088")
        return
    
    print("✅ Server is running")
    
    # Menu
    while True:
        print("\n" + "=" * 60)
        print("Choose an option:")
        print("1. Run complete pipeline")
        print("2. Check pipeline status")
        print("3. View execution history")
        print("4. View cost summary")
        print("5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            await test_pipeline()
        elif choice == "2":
            await check_pipeline_status()
        elif choice == "3":
            await get_pipeline_history()
        elif choice == "4":
            await get_cost_summary()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())