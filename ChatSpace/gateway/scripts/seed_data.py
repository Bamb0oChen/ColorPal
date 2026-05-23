import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import User, PhotoRecord, CommunityPost, CommunityComment, CommunityLike

Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()

    try:
        if db.query(User).count() > 0:
            print("数据已存在，跳过种子数据填充")
            return

        users_data = [
            {
                "id": "user_001",
                "nickname": "色彩探险家",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=colorpal"
            },
            {
                "id": "user_002",
                "nickname": "调色师小王",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=artist"
            },
            {
                "id": "user_003",
                "nickname": "城市漫步者",
                "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=walker"
            }
        ]

        users = []
        for data in users_data:
            user = User(**data)
            db.add(user)
            users.append(user)

        db.commit()

        photo_records_data = [
            {
                "id": str(uuid.uuid4()),
                "user_id": "user_001",
                "image_base64": "",
                "dominant_color": "#FF6B6B",
                "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D"],
                "score": 85,
                "comment": "红青互补，非常高级的配色！",
                "color_category": "warm",
                "saturation_level": "high",
                "brightness_level": "medium"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": "user_002",
                "image_base64": "",
                "dominant_color": "#4ECDC4",
                "palette": ["#4ECDC4", "#45B7D1", "#96CEB4"],
                "score": 90,
                "comment": "完美的青色调，和谐统一！",
                "color_category": "cool",
                "saturation_level": "medium",
                "brightness_level": "high"
            }
        ]

        photo_records = []
        for data in photo_records_data:
            pr = PhotoRecord(**data)
            db.add(pr)
            photo_records.append(pr)

        db.commit()

        posts_data = [
            {
                "id": str(uuid.uuid4()),
                "user_id": "user_001",
                "content": "今天在街头发现了这个超美的红色涂鸦！小人吃了超级开心～",
                "images": ["https://picsum.photos/seed/color1/400/300"],
                "photo_record_id": photo_records[0].id,
                "like_count": 24,
                "comment_count": 3
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": "user_002",
                "content": "今天的天空好清澈，拍下来分享给大家！这个青色调太治愈了",
                "images": ["https://picsum.photos/seed/color2/400/300", "https://picsum.photos/seed/color3/400/300"],
                "photo_record_id": photo_records[1].id,
                "like_count": 42,
                "comment_count": 7
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": "user_003",
                "content": "城市漫步发现的色彩，每一张照片都值得被珍藏！",
                "images": ["https://picsum.photos/seed/color4/400/300", "https://picsum.photos/seed/color5/400/300", "https://picsum.photos/seed/color6/400/300"],
                "like_count": 18,
                "comment_count": 2
            }
        ]

        posts = []
        for data in posts_data:
            post = CommunityPost(**data)
            db.add(post)
            posts.append(post)

        db.commit()

        comments_data = [
            {"post_id": posts[0].id, "user_id": "user_002", "content": "这个红色好正！"},
            {"post_id": posts[0].id, "user_id": "user_003", "content": "在哪里拍的？好想去看看！"},
            {"post_id": posts[0].id, "user_id": "user_001", "content": "谢谢喜欢！在市中心的老街上～"},
            {"post_id": posts[1].id, "user_id": "user_001", "content": "太治愈了！"},
            {"post_id": posts[1].id, "user_id": "user_003", "content": "这个配色90分当之无愧！"},
            {"post_id": posts[1].id, "user_id": "user_002", "content": "哈哈谢谢大家喜欢～"},
            {"post_id": posts[1].id, "user_id": "user_001", "content": "小人肯定超喜欢这个颜色！"}
        ]

        for data in comments_data:
            comment = CommunityComment(id=str(uuid.uuid4()), **data)
            db.add(comment)

        likes_data = [
            {"post_id": posts[0].id, "user_id": "user_002"},
            {"post_id": posts[0].id, "user_id": "user_003"},
            {"post_id": posts[1].id, "user_id": "user_001"},
            {"post_id": posts[1].id, "user_id": "user_003"},
            {"post_id": posts[2].id, "user_id": "user_001"},
            {"post_id": posts[2].id, "user_id": "user_002"}
        ]

        for data in likes_data:
            like = CommunityLike(id=str(uuid.uuid4()), **data)
            db.add(like)

        db.commit()

        print("种子数据填充完成！")

    except Exception as e:
        print(f"填充失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
