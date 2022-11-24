from django.db import models

class MovieInfo(models.Model):
    title = models.CharField(max_length=30)
    salesAmount = models.FloatField()
    salesShare = models.FloatField()
    salesInten = models.FloatField()
    salesChange = models.FloatField()
    salesAcc = models.FloatField()
    audiCnt = models.FloatField()
    audiInten = models.FloatField()
    audiChange = models.FloatField()
    audiAcc = models.FloatField()
    scrnCnt = models.FloatField()
    showCnt = models.FloatField()

    genres = models.TextField()
    nation = models.CharField(max_length=10)
    prodDate = models.CharField(max_length=8)
    openDate = models.CharField(max_length=8)
    companys = models.TextField()
    actors = models.TextField()
    directors = models.TextField()
    poster = models.TextField()
    link = models.TextField()
    
    ratingAudi = models.FloatField()
    ratingCritic = models.FloatField()
    ratingNetizen = models.FloatField()
    summaryContent = models.TextField()
    summaryNote = models.TextField()
    ratingNetizenM = models.FloatField()
    ratingNetizenF = models.FloatField()
    ratingNetizen10 = models.FloatField()
    ratingNetizen20 = models.FloatField()
    ratingNetizen30 = models.FloatField()
    ratingNetizen40 = models.FloatField()
    ratingNetizen50 = models.FloatField()
    ratingAudiM = models.FloatField()
    ratingAudiF = models.FloatField()
    ratingAudi10 = models.FloatField()
    ratingAudi20 = models.FloatField()
    ratingAudi30 = models.FloatField()
    ratingAudi40 = models.FloatField()
    ratingAudi50 = models.FloatField()
    ratingNetizenDir = models.PositiveSmallIntegerField()
    ratingNetizenAct = models.PositiveSmallIntegerField()
    ratingNetizenScn = models.PositiveSmallIntegerField()
    ratingNetizenMis = models.PositiveSmallIntegerField()
    ratingNetizenOst = models.PositiveSmallIntegerField()
    ratingAudiDir = models.PositiveSmallIntegerField()
    ratingAudiAct = models.PositiveSmallIntegerField()
    ratingAudiScn = models.PositiveSmallIntegerField()
    ratingAudiMis = models.PositiveSmallIntegerField()
    ratingAudiOst = models.PositiveSmallIntegerField()
    
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
