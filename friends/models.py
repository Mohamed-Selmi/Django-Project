from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
class FriendRequest(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    active_status=models.BooleanField(blank=False, null=False, default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username
    def AcceptFriendRequest(self):
      receiver_friendlist=FriendList.objects.get_or_create(user=self.receiver)
      print(receiver_friendlist[0])
      if receiver_friendlist:
        receiver_friendlist[0].add_friend(self.sender)
        sender_friendlist = FriendList.objects.get_or_create(user=self.sender)
        if sender_friendlist:
            sender_friendlist[0].add_friend(self.receiver)
            self.active_status=False
            self.save()
    def DeclineFriendRequest(self):
        self.active_status=False
        self.delete()
    def CancelFriendRequest(self):
        self.active_status=False
        self.delete()


class FriendList(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="User")
    friends=models.ManyToManyField(User, blank=True, related_name="friends")
    def __str__(self):
        return self.user.username
    def add_friend(self,friend):
        if not friend in self.friends.all():
            self.friends.add(friend)
            self.save()
    def remove_friend(self,friend):
        if friend in self.friends.all():
            self.friends.remove(friend)
    def unfriend(self,friend):
        self.remove_friend(friend)
        friend_list = FriendList.objects.get(user=friend)
        friend_list.remove_friend(self.user)
    def is_friend(self,friend):
        return self.friends.filter(user_id=friend.user_id).exists()
    def get_friends(self):
        return self.friends.all()
        