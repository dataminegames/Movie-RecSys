from django.db import models


class MovieInfo(models.Model):
    title = models.CharField(max_length=30)
    genres = models.CharField(max_length=20)
    nation = models.CharField(max_length=10)
    open_date = models.PositiveSmallIntegerField()
    companys = models.CharField(max_length=100)
    actors = models.TextField()
    directors = models.TextField()
    poster = models.TextField()
    link = models.TextField()
    rating_audi = models.FloatField()
    rating_critic = models.FloatField()
    rating_netizen = models.FloatField()
    audi_acc = models.PositiveSmallIntegerField()
    # description = models.TextField()

    def __str__(self):
        return self.title


class MovieChoice(models.Model):
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.movie.title


class UserProfile(models.Model):
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2)
    address = models.CharField(max_length=10)
    mbti = models.CharField(max_length=4)
    vote_date = models.DateTimeField()

    def __str__(self):
        return '{} / {}-{}-{}-{}'.format(str(self.vote_date)[:19], self.age, self.gender, self.address, self.mbti)


class UserLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(MovieInfo, on_delete=models.CASCADE)

    def __str__(self):
        return '{} / {}{}{}{} / {}'.format(str(self.user.vote_date)[:19], self.user.age, self.user.gender, self.user.address, self.user.mbti, self.movie.title)
