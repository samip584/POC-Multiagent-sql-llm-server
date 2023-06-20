"""Add dummy data - posts and timelines

Revision ID: 008
Revises: 007
Create Date: 2025-11-19 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert dummy posts
    op.execute("""
        INSERT INTO posts (user_id, media_id, caption, created_at, updated_at) VALUES
        (1, 1, 'Amazing mountain views! 🏔️ #nature #adventure', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days'),
        (1, 7, 'Beach sunset never gets old 🌅', NOW() - INTERVAL '8 days', NOW() - INTERVAL '8 days'),
        (2, 11, 'Modern architecture inspiration #design', NOW() - INTERVAL '9 days', NOW() - INTERVAL '9 days'),
        (2, 21, 'Coffee and code ☕💻 #developer', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'),
        (3, 15, 'Morning coffee ritual ☕', NOW() - INTERVAL '7 days', NOW() - INTERVAL '7 days'),
        (3, 18, 'Dinner at the best spot in town! 🍝', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (4, 14, 'Chicago skyline at dusk 🌆', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'),
        (4, 24, 'Getting my read on 📚', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (5, 26, 'New headshot for portfolio 📸', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (5, 2, 'Winter wonderland ❄️ #mountains', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (6, 34, 'Gym session complete 💪 #fitness', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (6, 38, 'Live music vibes 🎸', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (7, 15, 'Best coffee in Seattle ☕', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (7, 4, 'Forest bathing 🌲 #nature', NOW(), NOW()),
        (8, 7, 'Miami beach life 🌴', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (8, 28, 'Beach portrait session 📷', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (9, 1, 'Mountain hiking adventure 🥾', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (9, 9, 'Colorado wildflowers 🌸', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (10, 11, 'On set today 🎬 #filmmaker', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (10, 13, 'Urban exploration 🏙️', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (11, 34, 'Marathon training day 5 🏃', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (11, 35, 'Yoga morning routine 🧘', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (12, 16, 'Brunch goals 🥐', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'),
        (12, 39, 'Guitar practice 🎸', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (13, 8, 'Desert sunset magic 🌵', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (13, 10, 'Wildflower season! 🌺', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (14, 38, 'Atlanta music scene 🎵', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (14, 12, 'City lights 🌃', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (15, 21, 'Code review time 💻', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (15, 22, 'New workspace setup ⌨️', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (16, 7, 'Surfing paradise 🏄', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'),
        (16, 29, 'Beach portrait 📸', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (17, 38, 'Jazz night in NOLA 🎷', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (17, 17, 'Fresh produce market 🥬', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (18, 38, 'Austin live music 🎸', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (18, 18, 'Taco Tuesday! 🌮', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (19, 20, 'Office grind ⌨️', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (19, 13, 'DC monuments tour 🏛️', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (20, 21, 'Startup life 💡 #tech', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (20, 11, 'San Francisco vibes 🌁', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (21, 8, 'Lake views 🛶', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (21, 5, 'Minnesota nature 🌲', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
        (22, 20, 'Automotive design inspiration 🚗', NOW() - INTERVAL '6 days', NOW() - INTERVAL '6 days'),
        (22, 23, 'Research and development 📖', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (23, 9, 'Border town stories 📸', NOW() - INTERVAL '4 days', NOW() - INTERVAL '4 days'),
        (23, 17, 'Local cuisine 🌮', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (24, 21, 'Tech meetup today! 👨‍💻', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days'),
        (24, 22, 'New keyboard arrived ⌨️', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day'),
        (25, 16, 'Philly cheesesteak hunt 🥖', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
        (25, 25, 'Reading corner 📚', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days')
    """)
    
    # Insert dummy timelines
    op.execute("""
        INSERT INTO timelines (start_timestamp, end_timestamp, user_id, places_id) VALUES
        (1700000000, 1700003600, 1, '[1, 5]'),
        (1700100000, 1700110000, 1, '[2, 3]'),
        (1700200000, 1700205000, 2, '[2, 7]'),
        (1700300000, 1700310000, 2, '[14, 20]'),
        (1700400000, 1700408000, 3, '[3, 16]'),
        (1700500000, 1700515000, 3, '[3, 18]'),
        (1700600000, 1700610000, 4, '[4, 9]'),
        (1700700000, 1700720000, 4, '[4, 13]'),
        (1700800000, 1700808000, 5, '[1, 5, 23]'),
        (1700900000, 1700915000, 5, '[1, 21]'),
        (1701000000, 1701010000, 6, '[6, 25]'),
        (1701100000, 1701120000, 6, '[6]'),
        (1701200000, 1701208000, 7, '[7, 11]'),
        (1701300000, 1701315000, 7, '[7]'),
        (1701400000, 1701410000, 8, '[8, 15]'),
        (1701500000, 1701520000, 8, '[8]'),
        (1701600000, 1701608000, 9, '[9, 12]'),
        (1701700000, 1701715000, 9, '[9]'),
        (1701800000, 1701810000, 10, '[1, 5, 23]'),
        (1701900000, 1701920000, 10, '[5, 23]'),
        (1702000000, 1702008000, 11, '[10]'),
        (1702100000, 1702115000, 11, '[10]'),
        (1702200000, 1702210000, 12, '[11, 19]'),
        (1702300000, 1702320000, 12, '[11]'),
        (1702400000, 1702408000, 13, '[12]'),
        (1702500000, 1702515000, 13, '[12]'),
        (1702600000, 1702610000, 14, '[13, 24]'),
        (1702700000, 1702720000, 14, '[13]'),
        (1702800000, 1702808000, 15, '[14, 22]'),
        (1702900000, 1702915000, 15, '[14]'),
        (1703000000, 1703010000, 16, '[15]'),
        (1703100000, 1703120000, 16, '[15]'),
        (1703200000, 1703208000, 17, '[16]'),
        (1703300000, 1703315000, 17, '[16, 18]'),
        (1703400000, 1703410000, 18, '[17]'),
        (1703500000, 1703520000, 18, '[17]'),
        (1703600000, 1703608000, 19, '[18]'),
        (1703700000, 1703715000, 19, '[18]'),
        (1703800000, 1703810000, 20, '[2, 22]'),
        (1703900000, 1703920000, 20, '[2, 7]'),
        (1704000000, 1704008000, 21, '[19]'),
        (1704100000, 1704115000, 21, '[19]'),
        (1704200000, 1704210000, 22, '[20]'),
        (1704300000, 1704320000, 22, '[20]'),
        (1704400000, 1704408000, 23, '[6]'),
        (1704500000, 1704515000, 23, '[6, 25]'),
        (1704600000, 1704610000, 24, '[7, 11]'),
        (1704700000, 1704720000, 24, '[7]'),
        (1704800000, 1704808000, 25, '[10]'),
        (1704900000, 1704915000, 25, '[10, 20]')
    """)


def downgrade() -> None:
    op.execute("DELETE FROM timelines WHERE id BETWEEN 1 AND 50")
    op.execute("DELETE FROM posts WHERE id BETWEEN 1 AND 50")
