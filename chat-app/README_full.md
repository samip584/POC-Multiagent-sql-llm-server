# Chat App - Multi-Agent Chatbot Frontend

A modern, real-time chat interface built with React for interacting with the multi-agent LLM backend. Features include conversation history, image rendering, user context switching, and a sleek dark-mode UI.

## 🎨 Features

- **Real-time Chat Interface** - Conversational UI with message bubbles
- **Image Support** - Inline markdown images and grid gallery display
- **User Context** - Switch between different users to query their data
- **Chat History** - Maintains session-based conversation context (last 10 messages)
- **Example Queries** - Quick-access query suggestions
- **Loading States** - Animated dots while waiting for responses
- **Dark Mode UI** - Modern, eye-friendly interface
- **Responsive Design** - Works on desktop and mobile devices

## 🏗️ Architecture

### Component Structure

```
App (Main Container)
├── Header
│   ├── Title & Description
│   └── Example Queries (toggleable)
├── ChatArea
│   ├── Message List
│   │   ├── User Messages
│   │   └── Bot Messages
│   │       ├── Text Content (with markdown)
│   │       └── Image Gallery
│   └── Loading Indicator
└── InputArea
    ├── User Dropdown
    ├── Text Input
    └── Send Button
```

### State Management

The app uses React's `useState` and `useEffect` hooks for state management:

```javascript
{
  messages: [          // Chat message history
    {
      author: "user" | "bot",
      content: string,
      images: [{url, alt}],  // Only for bot messages
      hasImages: boolean      // Only for bot messages
    }
  ],
  users: [            // Available users from backend
    {id, name, email, ...}
  ],
  selectedUserId: number,    // Current user context
  isSending: boolean         // Loading state
}
```

## 🗄️ Database Schema (Backend)

The frontend interacts with the following PostgreSQL database schema through the backend API:

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    bio TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**

- `id` - Unique user identifier
- `username` - User's display name
- `email` - User's email address
- `bio` - User profile description
- `avatar_url` - Profile picture URL (MinIO)
- `created_at` - Account creation timestamp

### Posts Table

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    media_id INTEGER REFERENCES media(id) ON DELETE SET NULL,
    caption TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**

- `id` - Unique post identifier
- `user_id` - Author of the post (FK to users)
- `media_id` - Associated image/media (FK to media)
- `caption` - Post text content
- `timestamp` - Post creation time

### Media Table

```sql
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    external_resource_url TEXT NOT NULL,
    meta JSONB
);
```

**Fields:**

- `id` - Unique media identifier
- `external_resource_url` - MinIO S3 URL (e.g., `http://localhost:9000/media/photo1.jpg`)
- `meta` - JSON metadata: `{type, width, height, tags: []}`

**Example meta:**

```json
{
  "type": "image",
  "width": 1920,
  "height": 1280,
  "tags": ["portrait", "woman", "professional"]
}
```

### Places Table

```sql
CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address TEXT,
    category VARCHAR(50)
);
```

**Fields:**

- `id` - Unique place identifier
- `name` - Place/location name
- `description` - Details about the place
- `latitude` - Geographic coordinate
- `longitude` - Geographic coordinate
- `address` - Full street address
- `category` - Type (e.g., "restaurant", "park", "museum")

### Follows Table

```sql
CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    following_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(follower_id, following_id)
);
```

**Fields:**

- `id` - Unique follow relationship identifier
- `follower_id` - User who is following (FK to users)
- `following_id` - User being followed (FK to users)
- `timestamp` - When the follow occurred

**Constraints:**

- Prevents duplicate follow relationships
- Cascades delete when user is removed

### Timeline Table

```sql
CREATE TABLE timeline (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**

- `id` - Unique timeline entry identifier
- `user_id` - User whose timeline this appears on (FK to users)
- `post_id` - Post appearing on timeline (FK to posts)
- `timestamp` - When post appeared on timeline

**Purpose:** Aggregates posts for user feeds (posts from followed users)

### Entity Relationships

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Users   │────────>│  Posts   │────────>│  Media   │
│          │ 1:N     │          │ N:1     │          │
└────┬─────┘         └──────────┘         └──────────┘
     │
     │ Self-referencing
     │ (Follows)
     │
     └──> Follows <───┘
          (follower_id,
           following_id)

┌──────────┐
│ Timeline │─> References Users & Posts
└──────────┘   (Aggregated Feed)

┌──────────┐
│  Places  │   (Standalone location data)
└──────────┘
```

**Key Relationships:**

- One user can have many posts (1:N)
- One post has one media item (N:1)
- Users follow many users (M:N through follows)
- Timeline aggregates posts for user feeds (M:N)
- Places are independent entities (no direct FK)

### Sample Data Structure

**User with Posts and Images:**

```javascript
// Query: "Show me posts from user 1"
// Backend JOINs: users -> posts -> media

User {
  id: 1,
  username: "alice",
  email: "alice@example.com",
  bio: "Travel enthusiast",
  avatar_url: "http://localhost:9000/media/avatar1.jpg",
  posts: [
    {
      id: 1,
      caption: "Beautiful sunset!",
      timestamp: "2025-11-20T10:30:00Z",
      media: {
        id: 5,
        url: "http://localhost:9000/media/sunset.jpg",
        meta: {tags: ["nature", "sunset"]}
      }
    }
  ]
}
```

**Follow Relationships:**

```javascript
// Query: "Who follows user 1?"
[
  { follower_id: 2, follower_username: "bob" },
  { follower_id: 3, follower_username: "charlie" },
][
  // Query: "Who does user 1 follow?"
  ({ following_id: 4, following_username: "diana" },
  { following_id: 5, following_username: "eve" })
];
```

### Database Queries from Frontend

The chatbot performs SQL queries based on user questions:

**Example 1: Get posts with images**

```sql
-- User asks: "Show me posts with images"
SELECT p.id, p.caption, p.timestamp,
       u.username,
       m.external_resource_url, m.meta
FROM posts p
JOIN users u ON p.user_id = u.id
JOIN media m ON p.media_id = m.id
ORDER BY p.timestamp DESC;
```

**Example 2: Get user profile**

```sql
-- User asks: "Show me user 1's profile"
SELECT id, username, email, bio, avatar_url, created_at
FROM users
WHERE id = 1;
```

**Example 3: Get followers**

```sql
-- User asks: "Who follows me?" (as user 1)
SELECT u.id, u.username, u.avatar_url, f.timestamp
FROM follows f
JOIN users u ON f.follower_id = u.id
WHERE f.following_id = 1
ORDER BY f.timestamp DESC;
```

**Example 4: Get timeline/feed**

```sql
-- User asks: "Show my feed" (as user 1)
SELECT p.id, p.caption, p.timestamp,
       u.username,
       m.external_resource_url
FROM timeline t
JOIN posts p ON t.post_id = p.id
JOIN users u ON p.user_id = u.id
LEFT JOIN media m ON p.media_id = m.id
WHERE t.user_id = 1
ORDER BY t.timestamp DESC;
```

**Example 5: Recommend places**

```sql
-- User asks: "Recommend places for me"
SELECT id, name, description, category, address
FROM places
WHERE category IN ('restaurant', 'cafe', 'park')
ORDER BY RANDOM()
LIMIT 5;
```

## 📊 Data Flow

### 1. Initial Load

```
Component Mount
    ↓
Fetch Users (GET /users/)
    ↓
Set selectedUserId to first user
    ↓
Ready for chat
```

### 2. Send Message Flow

```
User types & clicks Send
    ↓
Add user message to state
    ↓
Build chat history (last 10 messages)
    ↓
POST /chat-bot/ask with:
  - question
  - user_id
  - include_images: true
  - chat_history: [{role, content}]
    ↓
Receive response:
  - text (markdown with images)
  - images: [{url, alt}]
  - has_images: boolean
    ↓
Add bot message to state
    ↓
Render response with images
```

### 3. Image Rendering

```
Bot Response Received
    ↓
Parse markdown images: ![alt](url)
    ↓
Render inline images in text
    ↓
If has_images=true, render gallery
    ↓
Display clickable image grid
```

## 🔌 API Integration

### Backend Endpoints

**GET /users/**

- Fetch all users for dropdown selection
- Response: `[{id, name, email, username, bio, avatar_url}]`

**POST /chat-bot/ask**

- Send question with context and history
- Request:

```json
{
  "question": "Show me posts with images",
  "user_id": 1,
  "include_images": true,
  "chat_history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ]
}
```

- Response:

```json
{
  "text": "Here are some posts:\n![Image 1](http://localhost:9000/media/1.jpg)",
  "images": [{ "url": "http://localhost:9000/media/1.jpg", "alt": "Image 1" }],
  "has_images": true,
  "user_id": 1
}
```

## 💬 Message Data Structure

### User Message

```javascript
{
  author: "user",
  content: "Show me all posts"
}
```

### Bot Message

```javascript
{
  author: "bot",
  content: "Hey! I found 5 posts:\n![Image 1](url1)\n![Image 2](url2)",
  images: [
    {url: "http://localhost:9000/media/1.jpg", alt: "Image 1"},
    {url: "http://localhost:9000/media/2.jpg", alt: "Image 2"}
  ],
  hasImages: true
}
```

### Chat History Format

```javascript
[
  { role: "user", content: "Show me posts" },
  { role: "assistant", content: "Here are the posts..." },
  { role: "user", content: "What about user 2?" },
];
```

## 🎨 UI Components

### Header

- **Title**: "POC MultiAgent"
- **Description**: "Your personal assistant with image support 📸"
- **Example Queries Button**: Toggles list of sample questions
- **Example Queries Grid**: 2-column grid with query suggestions

### ChatArea

- **Message Bubbles**: Alternating left (user) and right (bot) alignment
- **Inline Images**: Rendered from markdown `![alt](url)` syntax
- **Image Gallery**: Grid layout (auto-fill, min 200px columns)
- **Loading Indicator**: Animated dots while processing
- **Auto-scroll**: Maintains scroll position on new messages

### InputArea

- **User Dropdown**: Select user context (150px min-width)
- **Text Input**: Expandable input field with placeholder
- **Send Button**: Primary action with hover effects
- **Enter Key Support**: Submit message on Enter press
- **Disabled State**: UI disabled while sending

## 🎨 Styling

### Color Palette

```css
Background:     #121212 (dark)
Cards/Messages: #333333
UI Elements:    #1e1e1e, #2a2a2a
Accent:         #61dafb (cyan)
Text:           #e0e0e0, white
Borders:        #444444
```

### Key Animations

- **Dot Flashing**: Loading indicator (3 dots)
- **Shimmer**: Image loading state
- **Hover Effects**: Scale, shadow, transform on images
- **Button Transitions**: Color changes on hover

### Responsive Grid

```css
Image Gallery: repeat(auto-fill, minmax(200px, 1fr))
Example Queries: 2 columns fixed
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn
- Backend server running on `localhost:8000`

### Installation

1. **Install dependencies**:

```bash
npm install
```

2. **Start development server**:

```bash
npm start
```

App will open at `http://localhost:3000`

### Environment

The app expects the backend at:

```javascript
const BACKEND_URL = "http://localhost:8000";
```

To change this, update the fetch URLs in `App.js`:

```javascript
// Line ~18
fetch("http://localhost:8000/users/")

// Line ~37
fetch("http://localhost:8000/chat-bot/ask", ...)
```

## 📁 Project Structure

```
chat-app/
├── public/
│   ├── index.html          # HTML template
│   ├── manifest.json       # PWA manifest
│   └── robots.txt
├── src/
│   ├── App.js             # Main component ⭐
│   ├── App.css            # Styles ⭐
│   ├── index.js           # React entry point
│   ├── index.css          # Global styles
│   └── ...                # Test files
├── package.json
└── README.md
```

## 🔧 Configuration

### Message History Limit

Change the number of messages sent as context:

```javascript
// App.js line ~32
const chatHistory = messages.slice(-10); // Change -10 to desired limit
```

### Image Gallery Columns

Adjust grid columns in `App.css`:

```css
.image-gallery {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  /* Change 200px to desired min column width */
}
```

### Example Queries

Customize in `App.js` Header component:

```javascript
const exampleQueries = [
  "Show me all posts with images",
  "Your custom query here",
  // Add more...
];
```

## 🎯 Features Breakdown

### 1. Markdown Image Rendering

The `renderContent()` function parses markdown images:

```javascript
// Regex: ![alt](url)
const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
```

Images are rendered inline with error handling:

```javascript
<img
  src={imageUrl}
  alt={altText}
  onError={(e) => (e.target.style.display = "none")}
/>
```

### 2. Dual Image Display

**Inline**: Images from markdown in text flow
**Gallery**: Separate grid from `images` array

Both support:

- Click to open in new tab
- Hover zoom effect
- Error handling (hide on fail)
- Loading shimmer animation

### 3. User Context Switching

Users can switch perspective mid-conversation:

```javascript
<select onChange={(e) => onUserSelect(Number(e.target.value))}>
  {users.map((user) => (
    <option value={user.id}>{user.name}</option>
  ))}
</select>
```

Each message is sent with the selected `user_id`, allowing queries like:

- "Show me my posts" (as user 1)
- Switch to user 2
- "Show me my posts" (now returns user 2's posts)

### 4. Session Memory

Last 10 messages are sent with each request:

```javascript
const chatHistory = messages.slice(-10).map((msg) => ({
  role: msg.author === "user" ? "user" : "assistant",
  content: msg.content,
}));
```

This enables contextual follow-ups:

- User: "Show me posts"
- Bot: "Here are 5 posts..."
- User: "What about the first one?" ← Bot remembers context

## 🐛 Troubleshooting

### Images not loading

**Issue**: Gallery images show broken icon
**Fix**:

1. Check MinIO is running: `docker ps | grep minio`
2. Verify URL format: `http://localhost:9000/media/...`
3. Check browser console for CORS errors
4. Ensure MinIO bucket is public: `mc anonymous set download myminio/media`

### Chat history not working

**Issue**: Bot doesn't remember previous messages
**Fix**:

1. Check backend receives `chat_history` in request body
2. Verify backend logs show history processing
3. Ensure `messages` state is updating correctly
4. Check slice length: `messages.slice(-10)`

### User dropdown empty

**Issue**: No users in dropdown
**Fix**:

1. Backend running? `curl http://localhost:8000/users/`
2. Check browser console for fetch errors
3. Verify CORS enabled on backend
4. Check database has users: `SELECT * FROM users;`

### Send button not working

**Issue**: Nothing happens on click
**Fix**:

1. Check `isSending` state (should toggle)
2. Verify input has text: `question.trim()`
3. Look for errors in browser console
4. Check network tab for failed requests

## 📚 Technologies

- **React 18.2** - UI library
- **React Hooks** - State management (useState, useEffect)
- **Fetch API** - HTTP requests
- **CSS Grid** - Image gallery layout
- **CSS Flexbox** - Component layout
- **Markdown Parsing** - Regex-based image extraction

## 🎯 Future Enhancements

- [ ] Add typing indicators
- [ ] Support for more markdown (bold, italic, code)
- [ ] Message timestamps
- [ ] Copy message to clipboard
- [ ] Export chat history
- [ ] Dark/light mode toggle
- [ ] Voice input support
- [ ] Image zoom modal/lightbox
- [ ] Drag & drop image upload
- [ ] Message reactions/feedback
- [ ] Search through conversation
- [ ] Persistent storage (localStorage)

## 📝 Development Scripts

```bash
# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject (not recommended)
npm run eject
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT

---

Built with ❤️ using React
