"""Add dummy data - follows and media

Revision ID: 007
Revises: 006
Create Date: 2025-11-19 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert dummy media - focusing on people/portraits
    op.execute("""
        INSERT INTO media (external_resource_url, meta) VALUES
        ('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "professional"]}'),
        ('https://images.unsplash.com/photo-1494790108377-be9c29b29330', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "smile"]}'),
        ('https://images.unsplash.com/photo-1438761681033-6461ffad8d80', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "blonde"]}'),
        ('https://images.unsplash.com/photo-1500648767791-00dcc994a43e', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "outdoor"]}'),
        ('https://images.unsplash.com/photo-1522075469751-3a6694fb2f61', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "casual"]}'),
        ('https://images.unsplash.com/photo-1506794778202-cad84cf45f1d', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "beard"]}'),
        ('https://images.unsplash.com/photo-1534528741775-53994a69daeb', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "studio"]}'),
        ('https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "fashion"]}'),
        ('https://images.unsplash.com/photo-1531123897727-8f129e1688ce', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "professional"]}'),
        ('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "glasses"]}'),
        ('https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "smile"]}'),
        ('https://images.unsplash.com/photo-1544005313-94ddf0286df2', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "beauty"]}'),
        ('https://images.unsplash.com/photo-1546961329-78bef0414d7c', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "urban"]}'),
        ('https://images.unsplash.com/photo-1552058544-f2b08422138a', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "hoodie"]}'),
        ('https://images.unsplash.com/photo-1557862921-37829c790f19', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "business"]}'),
        ('https://images.unsplash.com/photo-1580489944761-15a19d654956', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "curly"]}'),
        ('https://images.unsplash.com/photo-1599566150163-29194dcaad36', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "beard"]}'),
        ('https://images.unsplash.com/photo-1601455763557-db1bea8a9a5a', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "brunette"]}'),
        ('https://images.unsplash.com/photo-1524504388940-b1c1722653e1', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "smile"]}'),
        ('https://images.unsplash.com/photo-1531384441138-2736e62e0919', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "happy"]}'),
        ('https://images.unsplash.com/photo-1519085360753-af0119f7cbe7', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "professional"]}'),
        ('https://images.unsplash.com/photo-1521119989659-a83eee488004', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "redhead"]}'),
        ('https://images.unsplash.com/photo-1558203728-00f45181dd84', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "casual"]}'),
        ('https://images.unsplash.com/photo-1570295999919-56ceb5ecca61', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "studio"]}'),
        ('https://images.unsplash.com/photo-1541216970279-affbfdd55aa8', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "natural"]}'),
        ('https://images.unsplash.com/photo-1603415526960-f7e0328c63b1', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "fashion"]}'),
        ('https://images.unsplash.com/photo-1566492031773-4f4e44671857', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "outdoor"]}'),
        ('https://images.unsplash.com/photo-1525974160448-038dacadcc71', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "smile"]}'),
        ('https://images.unsplash.com/photo-1463453091185-61582044d556', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "man", "beard"]}'),
        ('https://images.unsplash.com/photo-1539571696357-5a69c17a67c6', '{"type": "image", "width": 1920, "height": 1280, "tags": ["portrait", "woman", "professional"]}'),
        ('https://images.unsplash.com/photo-1492562080023-ab3db95bfbce', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "friends", "happy"]}'),
        ('https://images.unsplash.com/photo-1529111290557-82f6d5c6cf85', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "friends", "outdoor"]}'),
        ('https://images.unsplash.com/photo-1511632765486-a01980e01a18', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "party", "celebration"]}'),
        ('https://images.unsplash.com/photo-1543269865-cbf427effbad', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "team", "office"]}'),
        ('https://images.unsplash.com/photo-1543269664-56d93c1b41a6', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "meeting", "business"]}'),
        ('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "team", "diverse"]}'),
        ('https://images.unsplash.com/photo-1522071820081-009f0129c71c', '{"type": "image", "width": 1920, "height": 1280, "tags": ["group", "team", "collaboration"]}'),
        ('https://images.unsplash.com/photo-1528605248644-14dd04022da1', '{"type": "image", "width": 1920, "height": 1280, "tags": ["couple", "love", "outdoor"]}'),
        ('https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2', '{"type": "image", "width": 1920, "height": 1280, "tags": ["couple", "romantic", "sunset"]}'),
        ('https://images.unsplash.com/photo-1502086223501-7ea6ecd79368', '{"type": "image", "width": 1920, "height": 1280, "tags": ["couple", "happy", "beach"]}')
    """)
    
    # Insert dummy follows (creating social connections)
    op.execute("""
        INSERT INTO follow (source_user_id, destination_user_id) VALUES
        (1, 2), (1, 3), (1, 5), (1, 7), (1, 10),
        (2, 1), (2, 4), (2, 6), (2, 8), (2, 20),
        (3, 1), (3, 2), (3, 9), (3, 11), (3, 15),
        (4, 2), (4, 6), (4, 12), (4, 14), (4, 16),
        (5, 1), (5, 3), (5, 7), (5, 10), (5, 18),
        (6, 2), (6, 4), (6, 8), (6, 13), (6, 17),
        (7, 1), (7, 5), (7, 9), (7, 12), (7, 19),
        (8, 2), (8, 6), (8, 11), (8, 15), (8, 21),
        (9, 3), (9, 7), (9, 13), (9, 16), (9, 22),
        (10, 1), (10, 5), (10, 14), (10, 18), (10, 23),
        (11, 3), (11, 8), (11, 15), (11, 19), (11, 24),
        (12, 4), (12, 7), (12, 16), (12, 20), (12, 25),
        (13, 6), (13, 9), (13, 17), (13, 21), (13, 1),
        (14, 4), (14, 10), (14, 18), (14, 22), (14, 2),
        (15, 3), (15, 11), (15, 19), (15, 23), (15, 5),
        (16, 4), (16, 12), (16, 20), (16, 24), (16, 7),
        (17, 6), (17, 13), (17, 21), (17, 25), (17, 9),
        (18, 5), (18, 10), (18, 14), (18, 22), (18, 11),
        (19, 7), (19, 11), (19, 15), (19, 23), (19, 13),
        (20, 2), (20, 12), (20, 16), (20, 24), (20, 15)
    """)


def downgrade() -> None:
    op.execute("DELETE FROM follow WHERE id BETWEEN 1 AND 100")
    op.execute("DELETE FROM media WHERE id BETWEEN 1 AND 40")
