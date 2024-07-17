"""Add dummy data - users and places

Revision ID: 006
Revises: 005
Create Date: 2025-11-19 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert dummy users
    op.execute("""
        INSERT INTO users (name, email, phone, longitude, latitude, idp_id, bio, avatar_url) VALUES
        ('Alice Johnson', 'alice.j@email.com', 5551234567, -118.2437, 34.0522, 1001, 'Adventure seeker and coffee lover ☕', 'https://i.pravatar.cc/150?img=1'),
        ('Bob Smith', 'bob.smith@email.com', 5552345678, -122.4194, 37.7749, 1002, 'Tech enthusiast | San Francisco', 'https://i.pravatar.cc/150?img=2'),
        ('Carol Davis', 'carol.d@email.com', 5553456789, -73.9352, 40.7306, 1003, 'NYC foodie 🍕 | Travel blogger', 'https://i.pravatar.cc/150?img=3'),
        ('David Lee', 'david.lee@email.com', 5554567890, -87.6298, 41.8781, 1004, 'Chicago deep dish advocate', 'https://i.pravatar.cc/150?img=4'),
        ('Emma Wilson', 'emma.w@email.com', 5555678901, -118.2437, 34.0522, 1005, 'Photographer | LA based', 'https://i.pravatar.cc/150?img=5'),
        ('Frank Martinez', 'frank.m@email.com', 5556789012, -95.3698, 29.7604, 1006, 'Houston, TX | Sports fan', 'https://i.pravatar.cc/150?img=6'),
        ('Grace Taylor', 'grace.t@email.com', 5557890123, -122.3321, 47.6062, 1007, 'Seattle coffee roaster', 'https://i.pravatar.cc/150?img=7'),
        ('Henry Brown', 'henry.b@email.com', 5558901234, -80.1918, 25.7617, 1008, 'Miami beach life 🌴', 'https://i.pravatar.cc/150?img=8'),
        ('Isabella Garcia', 'isabella.g@email.com', 5559012345, -104.9903, 39.7392, 1009, 'Denver mountains 🏔️', 'https://i.pravatar.cc/150?img=9'),
        ('Jack Anderson', 'jack.a@email.com', 5550123456, -118.2437, 34.0522, 1010, 'Film director | LA', 'https://i.pravatar.cc/150?img=10'),
        ('Kate Thompson', 'kate.t@email.com', 5551234560, -71.0589, 42.3601, 1011, 'Boston marathon runner', 'https://i.pravatar.cc/150?img=11'),
        ('Liam White', 'liam.w@email.com', 5552345670, -122.6765, 45.5231, 1012, 'Portland craft beer enthusiast', 'https://i.pravatar.cc/150?img=12'),
        ('Mia Harris', 'mia.h@email.com', 5553456780, -112.0740, 33.4484, 1013, 'Phoenix desert explorer', 'https://i.pravatar.cc/150?img=13'),
        ('Noah Martin', 'noah.m@email.com', 5554567891, -84.3880, 33.7490, 1014, 'Atlanta music scene', 'https://i.pravatar.cc/150?img=14'),
        ('Olivia Jackson', 'olivia.j@email.com', 5555678902, -121.8863, 37.3382, 1015, 'Silicon Valley engineer', 'https://i.pravatar.cc/150?img=15'),
        ('Peter Clark', 'peter.c@email.com', 5556789013, -157.8583, 21.3099, 1016, 'Honolulu surfer 🏄', 'https://i.pravatar.cc/150?img=16'),
        ('Quinn Rodriguez', 'quinn.r@email.com', 5557890124, -90.0715, 29.9511, 1017, 'New Orleans jazz lover', 'https://i.pravatar.cc/150?img=17'),
        ('Rachel Lewis', 'rachel.l@email.com', 5558901235, -97.7431, 30.2672, 1018, 'Austin live music fanatic', 'https://i.pravatar.cc/150?img=18'),
        ('Samuel Walker', 'samuel.w@email.com', 5559012346, -77.0369, 38.9072, 1019, 'DC politics watcher', 'https://i.pravatar.cc/150?img=19'),
        ('Tina Hall', 'tina.h@email.com', 5550123457, -122.4194, 37.7749, 1020, 'SF tech startup founder', 'https://i.pravatar.cc/150?img=20'),
        ('Ulysses Allen', 'ulysses.a@email.com', 5551234561, -93.2650, 44.9778, 1021, 'Minneapolis lakes enthusiast', 'https://i.pravatar.cc/150?img=21'),
        ('Vera Young', 'vera.y@email.com', 5552345671, -83.0458, 42.3314, 1022, 'Detroit automotive historian', 'https://i.pravatar.cc/150?img=22'),
        ('Walter King', 'walter.k@email.com', 5553456781, -106.4424, 31.7619, 1023, 'El Paso border town stories', 'https://i.pravatar.cc/150?img=23'),
        ('Xena Scott', 'xena.s@email.com', 5554567892, -122.3321, 47.6062, 1024, 'Seattle tech scene', 'https://i.pravatar.cc/150?img=24'),
        ('Yuri Green', 'yuri.g@email.com', 5555678903, -75.1652, 39.9526, 1025, 'Philadelphia cheesesteak expert', 'https://i.pravatar.cc/150?img=25')
    """)
    
    # Insert dummy places
    op.execute("""
        INSERT INTO places (longitude, latitude, title, category, description, address) VALUES
        (-118.2437, 34.0522, 'Griffith Observatory', 'Attraction', 'Iconic observatory with city views', '2800 E Observatory Rd, Los Angeles, CA 90027'),
        (-122.4194, 37.7749, 'Golden Gate Bridge', 'Landmark', 'Famous suspension bridge', 'Golden Gate Bridge, San Francisco, CA'),
        (-73.9352, 40.7306, 'Brooklyn Bridge', 'Landmark', 'Historic NYC bridge', 'Brooklyn Bridge, New York, NY 10038'),
        (-87.6298, 41.8781, 'Millennium Park', 'Park', 'Urban park with Cloud Gate', '201 E Randolph St, Chicago, IL 60602'),
        (-118.3005, 34.1341, 'Universal Studios', 'Entertainment', 'Movie theme park', '100 Universal City Plaza, Universal City, CA 91608'),
        (-95.3698, 29.7604, 'Space Center Houston', 'Museum', 'NASA visitor center', '1601 E NASA Pkwy, Houston, TX 77058'),
        (-122.3321, 47.6205, 'Pike Place Market', 'Market', 'Historic farmers market', '85 Pike St, Seattle, WA 98101'),
        (-80.1300, 25.7907, 'South Beach', 'Beach', 'Famous Miami beach', 'Ocean Dr, Miami Beach, FL 33139'),
        (-104.9847, 39.7294, 'Red Rocks Park', 'Park', 'Natural amphitheatre', '18300 W Alameda Pkwy, Morrison, CO 80465'),
        (-71.0589, 42.3601, 'Freedom Trail', 'Historic', 'Revolutionary War sites', 'Boston, MA 02108'),
        (-122.6765, 45.5152, 'Powell''s City of Books', 'Bookstore', 'World''s largest bookstore', '1005 W Burnside St, Portland, OR 97209'),
        (-112.0740, 33.4484, 'Desert Botanical Garden', 'Garden', 'Desert plant showcase', '1201 N Galvin Pkwy, Phoenix, AZ 85008'),
        (-84.3880, 33.7490, 'World of Coca-Cola', 'Museum', 'Coca-Cola history museum', '121 Baker St NW, Atlanta, GA 30313'),
        (-121.8863, 37.3382, 'Computer History Museum', 'Museum', 'Tech history exhibits', '1401 N Shoreline Blvd, Mountain View, CA 94043'),
        (-157.8583, 21.2793, 'Waikiki Beach', 'Beach', 'Famous Hawaiian beach', 'Waikiki Beach, Honolulu, HI 96815'),
        (-90.0715, 29.9584, 'French Quarter', 'Historic', 'Historic New Orleans district', 'French Quarter, New Orleans, LA 70116'),
        (-97.7431, 30.2672, 'Lady Bird Lake', 'Nature', 'Urban lake and trail', 'Lady Bird Lake, Austin, TX 78704'),
        (-77.0369, 38.8977, 'National Mall', 'Landmark', 'Iconic DC monuments', 'National Mall, Washington, DC 20560'),
        (-93.2650, 44.9537, 'Minneapolis Sculpture Garden', 'Art', 'Outdoor sculpture park', '725 Vineland Pl, Minneapolis, MN 55403'),
        (-83.0458, 42.3314, 'Detroit Institute of Arts', 'Museum', 'World-class art museum', '5200 Woodward Ave, Detroit, MI 48202'),
        (-118.4912, 34.0195, 'Santa Monica Pier', 'Entertainment', 'Iconic beach pier', '200 Santa Monica Pier, Santa Monica, CA 90401'),
        (-122.4783, 37.8199, 'Alcatraz Island', 'Historic', 'Former federal prison', 'Alcatraz Island, San Francisco, CA 94133'),
        (-118.2851, 34.1015, 'Hollywood Sign', 'Landmark', 'Iconic LA landmark', 'Hollywood Sign, Los Angeles, CA 90068'),
        (-87.6244, 41.8369, 'Navy Pier', 'Entertainment', 'Lakefront entertainment', '600 E Grand Ave, Chicago, IL 60611'),
        (-95.3587, 29.7589, 'Museum of Fine Arts Houston', 'Museum', 'Major art museum', '1001 Bissonnet St, Houston, TX 77005')
    """)


def downgrade() -> None:
    op.execute("DELETE FROM places WHERE id BETWEEN 1 AND 25")
    op.execute("DELETE FROM users WHERE id BETWEEN 1 AND 25")
