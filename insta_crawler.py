import re
import instaloader
from datetime import datetime, timedelta


class InstaCrawler:
    def __init__(self, insta_account, insta_password, url):
        insta = instaloader.Instaloader()
        insta.login(insta_account, insta_password)
        acc = re.findall(r"https://www.instagram.com/(.+)/", url)[0]
        self.insta_profile = instaloader.Profile.from_username(insta.context, acc)

    def _get_user_profile(self):
        profile = {}
        profile["id"] = self.insta_profile.userid
        profile["follower_count"] = self.insta_profile.followers
        profile["biography"] = self.insta_profile.biography
        profile["username"] = self.insta_profile.username
        return profile

    def _get_posts(self):
        all_posts = self.insta_profile.get_posts()
        posts = []
        month_ago = datetime.now() + timedelta(days=-30)
        for post in all_posts:
            info = {}
            if post.date_local < month_ago:
                break
            try:
                info["id"] = post.mediaid
                info["shortcode"] = post.shortcode
                info["display_url"] = post.url
                info["like_count"] = post.likes
                info["comment_count"] = post.comments
                info["is_video"] = post.is_video
                info["taken_at_timestamp"] = int(post.date_local.timestamp())
                posts.append(info)
            except Exception as e:
                print(f"collect fail because {e}")
                pass
        return posts

    def get_data(self, profile, posts):
        data = {}
        data["profile"] = profile
        data["posts"] = posts
        return data


if __name__ == "__main__":
    insta = InstaCrawler(
        "YOUR_ACCOUNT", "YOUR_PASSWORD", "https://www.instagram.com/YOUR_URL/"
    )
    data = insta.get_data(insta._get_user_profile(), insta._get_posts())
