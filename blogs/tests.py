from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post, Comment

class BlogAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass456')

        self.client.login(username='user1', password='pass123')  # optional (only for browser login-based tests)

        # Get token for authorization
        token_res = self.client.post(reverse('token'), {
            'username': 'user1',
            'password': 'pass123'
        })
        self.access_token = token_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.post_data = {
            'title': 'First Post',
            'content': 'This is the content'
        }

    # Tests if the post creation endpoint works correctly
    def test_create_post(self):
        res = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    # Tests if all posts can be retrieved correctly
    def test_retrieve_posts_list(self):
        Post.objects.create(title='Test Post', content='Sample', author=self.user)
        res = self.client.get('/api/posts/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    # Test if a post can be updated by its author
    def test_update_post_as_author(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        update_data = {'title': 'Updated', 'content': 'New content'}
        res = self.client.put(f'/api/posts/{post.id}/', update_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Updated')

    # Ensures a post cannot be updated by a non-author
    def test_update_post_as_non_author(self):
        post = Post.objects.create(**self.post_data, author=self.other_user)
        res = self.client.put(f'/api/posts/{post.id}/', {
            'title': 'Hack',
            'content': 'Should not work'
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # Ensures a post can be deleted by its author
    def test_delete_post_as_author(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        res = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    
    # Ensures a post cannot be deleted by a non-author
    def test_delete_post_unauthenticated(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        self.client.credentials()
        res = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # Checks likes/unlikes functionality works correctly
    def test_toggle_like(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        res = self.client.post(f'/api/posts/{post.id}/toggle_like/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['likes count'], 1)

        # Unlike again
        res = self.client.post(f'/api/posts/{post.id}/toggle_like/')
        self.assertEqual(res.data['likes count'], 0)

    # Ensures a post cannot be liked by an unauthenticated user
    def test_like_post_unauthenticated(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        self.client.credentials()
        res = self.client.post(f'/api/posts/{post.id}/toggle_like/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


    # Checks if the likes list can be retrieved correctly
    def test_view_likes_list(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        post.likes.add(self.user)
        res = self.client.get(f'/api/posts/{post.id}/likes/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['username'], self.user.username)

    # Tests if comments can be created on a post
    def test_create_comment(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        res = self.client.post(f'/api/posts/{post.id}/comments/', {'text': 'Great post!'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    # Tests if comments can get listed correctly
    def test_list_comments(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        Comment.objects.create(post=post, author=self.user, text='Nice!')
        res = self.client.get(f'/api/posts/{post.id}/comments/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    # Tests if a comment can be updated by its author
    def test_update_comment_as_author(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        comment = Comment.objects.create(post=post, author=self.user, text="Original")
        res = self.client.put(f'/api/posts/{post.id}/comments/{comment.id}/', {
            "text": "Updated text"
        }, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["text"], "Updated text")

    # Ensures a comment cannot be updated by a non-author
    def test_update_comment_as_non_author(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        comment = Comment.objects.create(post=post, author=self.other_user, text="Not yours")
        res = self.client.put(f'/api/posts/{post.id}/comments/{comment.id}/', {
            "text": "Hacked"
        }, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    # Ensures a comment cannot be updated by unauthenticated user
    def test_update_comment_unauthenticated(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        comment = Comment.objects.create(post=post, author=self.user, text="Mine")
        self.client.credentials()
        res = self.client.put(f'/api/posts/{post.id}/comments/{comment.id}/', {
            "text": "Unauth edit"
        }, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # Ensures comment cannot be deleted by a unauthenticated user
    def test_delete_comment_unauthenticated(self):
        post = Post.objects.create(**self.post_data, author=self.user)
        comment = Comment.objects.create(post=post, author=self.user, text="Will be deleted")
        self.client.credentials()
        res = self.client.delete(f'/api/posts/{post.id}/comments/{comment.id}/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # Ensures user can see their own posts
    def test_my_posts_list(self):
        Post.objects.create(title='Mine', content='My post', author=self.user)
        Post.objects.create(title='Not mine', content='Other post', author=self.other_user)
        res = self.client.get('/api/posts/my_posts/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['author'], self.user.username)

    # Ensures user cannot create a post without authentication
    def test_unauthenticated_post_creation(self):
        self.client.credentials()  # remove auth
        res = self.client.post('/api/posts/', self.post_data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)