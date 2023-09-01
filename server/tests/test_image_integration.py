"""
Test examples for MinIO image integration
Run these after starting the Docker containers
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_posts_with_images():
    """Test querying posts with images"""
    print("\n=== Testing Posts with Images ===")
    
    response = requests.post(
        f"{BASE_URL}/chat-bot/ask",
        json={
            "question": "Show me all posts with their images",
            "user_id": 1,
            "include_images": True
        }
    )
    
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"\nText Response:\n{data['text']}\n")
    print(f"Has Images: {data['has_images']}")
    print(f"Number of Images: {len(data['images'])}")
    
    if data['images']:
        print("\nImage URLs:")
        for img in data['images']:
            print(f"  - {img['url']} (alt: {img['alt']})")
    
    return data


def test_user_with_avatar():
    """Test querying user with avatar"""
    print("\n=== Testing User Profile with Avatar ===")
    
    response = requests.post(
        f"{BASE_URL}/chat-bot/ask",
        json={
            "question": "Show me user 1's profile",
            "user_id": 1,
            "include_images": True
        }
    )
    
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"\nResponse:\n{data['text']}\n")
    print(f"Has Images: {data['has_images']}")
    
    return data


def test_simple_endpoint():
    """Test backward compatible simple endpoint"""
    print("\n=== Testing Simple Endpoint (Backward Compatible) ===")
    
    response = requests.post(
        f"{BASE_URL}/chat-bot/ask/simple",
        json={
            "question": "Show me recent posts",
            "user_id": 1
        }
    )
    
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"\nSimple Response:\n{data['response']}\n")
    
    return data


def test_no_images_query():
    """Test query that doesn't involve images"""
    print("\n=== Testing Non-Image Query ===")
    
    response = requests.post(
        f"{BASE_URL}/chat-bot/ask",
        json={
            "question": "How many users are there?",
            "user_id": 1,
            "include_images": True
        }
    )
    
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"\nResponse:\n{data['text']}\n")
    print(f"Has Images: {data['has_images']} (should be False)")
    
    return data


def test_cached_query():
    """Test that second query is cached and faster"""
    print("\n=== Testing Cache Performance ===")
    
    import time
    
    # First query
    start = time.time()
    response1 = requests.post(
        f"{BASE_URL}/chat-bot/ask",
        json={
            "question": "Show me all users",
            "user_id": 1
        }
    )
    time1 = time.time() - start
    
    # Second query (should be cached)
    start = time.time()
    response2 = requests.post(
        f"{BASE_URL}/chat-bot/ask",
        json={
            "question": "Show me all users",
            "user_id": 1
        }
    )
    time2 = time.time() - start
    
    print(f"First query: {time1:.2f}s")
    print(f"Second query (cached): {time2:.2f}s")
    print(f"Speedup: {(time1/time2):.1f}x faster")
    
    return time1, time2


def render_markdown_in_terminal(text):
    """Simple markdown renderer for terminal"""
    import re
    
    # Extract and display images
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)
    
    if images:
        print("\n📸 Images found:")
        for alt, url in images:
            print(f"  [{alt}] {url}")
    
    # Remove markdown image syntax for cleaner display
    clean_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'[Image: \1]', text)
    print(f"\n{clean_text}")


if __name__ == "__main__":
    print("🚀 Starting MinIO Image Integration Tests")
    print("=" * 60)
    
    try:
        # Test 1: Posts with images
        result1 = test_posts_with_images()
        
        # Test 2: User profile
        result2 = test_user_with_avatar()
        
        # Test 3: Simple endpoint
        result3 = test_simple_endpoint()
        
        # Test 4: Non-image query
        result4 = test_no_images_query()
        
        # Test 5: Cache performance
        test_cached_query()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server at", BASE_URL)
        print("Make sure Docker containers are running:")
        print("  cd /path/to/server && docker compose up")
    except Exception as e:
        print(f"\n❌ Error: {e}")


# Frontend integration example
FRONTEND_EXAMPLE = """
// React Component Example
function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const askQuestion = async () => {
    const response = await fetch('http://localhost:8000/chat-bot/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question: input,
        user_id: 1,
        include_images: true
      })
    });
    
    const data = await response.json();
    setMessages([...messages, data]);
    setInput('');
  };
  
  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className="message">
            <ReactMarkdown>{msg.text}</ReactMarkdown>
            
            {msg.has_images && (
              <div className="image-gallery">
                {msg.images.map((img, i) => (
                  <img key={i} src={img.url} alt={img.alt} />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <input 
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
        placeholder="Ask about posts, users, places..."
      />
    </div>
  );
}
"""

print(f"\n\n📱 Frontend Integration Example:\n{FRONTEND_EXAMPLE}")
